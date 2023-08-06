# NOTE: The functions in this file are not tested in chalkpy
# The integration tests in engine/ validate the behavior of load_dataset
from __future__ import annotations

import base64
import json
from collections import OrderedDict
from concurrent.futures import Future, ThreadPoolExecutor
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Union, cast

from typing_extensions import assert_never

from chalk.client.models import ColumnMetadata
from chalk.features import Feature, FeatureWrapper, deserialize_dtype, ensure_feature
from chalk.features._encoding.pyarrow import pyarrow_to_polars
from chalk.features.feature_set import FeatureSetBase
from chalk.features.pseudofeatures import CHALK_TS_FEATURE, ID_FEATURE, OBSERVED_AT_FEATURE, PSEUDONAMESPACE
from chalk.utils.collections import get_unique_item
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl


_DEFAULT_EXECUTOR = ThreadPoolExecutor(16)


class ColNameDecoder:
    def decode_col_name(self, col_name: str) -> str:
        if col_name.startswith("__") and col_name.endswith("__"):
            return col_name
        x_split = col_name.split("_")
        if x_split[0] == "ca":
            return "_".join(x_split[1:])
        elif x_split[0] == "cb":
            root_fqn_b32 = x_split[1]
            return base64.b32decode(root_fqn_b32.replace("0", "=").upper()).decode("utf8")
        elif x_split[0] == "cc":
            # Need to implement serialization / deserialization of the state dict
            raise NotImplementedError("Decoding stateful column names are not yet supported")
        else:
            raise ValueError(f"Unexpected identifier: {x_split[0]}")


class DatasetVersion(IntEnum):
    """Format of the parquet file. Used when loading a dataset so that we know what format it is in"""

    # This is the format that bigquery dumps to when specifying an output bucket and output format
    # as part of an (async) query job
    # The output contains extra columns, and all column names are b32 encoded, because
    # bigquery does not support '.' in column names.
    # The client will have to decode column names before loading this data
    # All data, except for feature times, are json encoded
    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES = 1

    # This is the format returned by the dataset writer in engine/
    DATASET_WRITER = 2

    # This format uses separate columns for the observed at and timestamp columns
    # The observed at column is the actual timestamp from when the observation was observed,
    # whereas the timestamp column is the original timestamp that the user requested
    BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2 = 3

    COMPUTE_RESOLVER_OUTPUT_V1 = 4

    NATIVE_DTYPES = 5
    """This format has feature values decoded with their native data types.
    It does not require json decoding client-side"""


def _parallel_download(uris: List[str], executor: ThreadPoolExecutor, lazy: bool) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")

    df_futures: list[Future[pl.LazyFrame] | Future[pl.DataFrame]] = []
    for uri in uris:
        if lazy:
            df_futures.append(executor.submit(pl.scan_parquet, uri))
        else:
            df_futures.append(executor.submit(pl.read_parquet, uri))

    dfs = [df.result() for df in df_futures]
    dfs = [x.select(sorted(x.columns)) for x in dfs]
    # Cast the list to be homogenous
    dfs = cast(Union[List[pl.DataFrame], List[pl.LazyFrame]], dfs)
    df = pl.concat(dfs)
    return df


def _load_dataset_from_chalk_writer(uris: List[str]) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    # V1 datasets should contain just a single URI
    # This URI can be read directly
    # We need to filter the features to remove any pseudofeatures
    if len(uris) != 1:
        raise ValueError("v1 datasets should have just a single URI")
    df = pl.read_parquet(uris[0])
    return df


def _decode_column_names(
    column_names: List[str],
) -> Mapping[str, str]:
    ans: Dict[str, str] = {}
    col_name_decoder = ColNameDecoder()
    for x in column_names:
        if x.startswith("__"):
            if x in ("__id__", ID_FEATURE.fqn):
                ans[x] = ID_FEATURE.fqn
            elif x in ("__ts__", CHALK_TS_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = CHALK_TS_FEATURE.fqn
            elif x in ("__observed_at__", "__oat__", OBSERVED_AT_FEATURE.fqn):
                # Preserve these columns as-is to help with loading the timestamp
                ans[x] = OBSERVED_AT_FEATURE.fqn
            # Drop all the other metadata columns
            continue
        feature_name = col_name_decoder.decode_col_name(x)
        if any(feature_name.endswith(f".__{x}__") for x in ("oat", "rat", "observed_at", "replaced_observed_at")):
            # Drop the timestamp metadata from individual features
            continue
        ans[x] = feature_name
    return ans


def _json_decode(x: Optional[str]):
    if x is None:
        return None
    return json.loads(x)


def _load_dataset_bigquery(
    uris: List[str],
    executor: Optional[ThreadPoolExecutor],
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: bool,
    output_id: bool,
    version: DatasetVersion,
    lazy: bool,
    columns: Optional[Sequence[ColumnMetadata]],
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # unused
    # V2 datasets are in multiple files, and have column names encoded
    # due to DB limitations (e.g. bigquery does not support '.' in column names)
    # In addition, the datasets may contain extra columns (e.g. replaced observed at)
    # All values are JSON encoded
    if executor is None:
        executor = _DEFAULT_EXECUTOR
    df = _parallel_download(uris, executor, lazy)
    return _extract_df_columns(df, output_feature_fqns, output_ts, output_id, version, columns)


def _extract_df_columns(
    df: Union[pl.DataFrame, pl.LazyFrame],
    output_feature_fqns: Optional[Sequence[str]],
    output_ts: bool,
    output_id: bool,
    version: DatasetVersion,
    column_metadata: Optional[Sequence[ColumnMetadata]] = None,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.NATIVE_DTYPES,
    ):
        decoded_col_names = _decode_column_names(df.columns)

        # Select only the columns in decoded_col_names
        df = df.select(list(decoded_col_names.keys()))
        df = df.rename(dict(decoded_col_names))

        # Using an OrderedDict so the order will match the order the user set in the
        # output argument
        expected_cols: Dict[str, pl.Expr] = OrderedDict()
        id_col = pl.col(str(ID_FEATURE))
        if output_id:
            # All dataframes have an __id__ column
            expected_cols[str(ID_FEATURE)] = id_col.alias(str(ID_FEATURE))

        ts_col = pl.col(str(OBSERVED_AT_FEATURE)).fill_null(pl.col(str(CHALK_TS_FEATURE))).dt.with_time_zone("UTC")
        if output_ts:
            # For the ts feature, we want `__oat__` if not null else `__ts__`
            # it is not null; otherwise, we want
            expected_cols[str(CHALK_TS_FEATURE)] = ts_col.alias(str(CHALK_TS_FEATURE))

        if output_feature_fqns is None:
            # If not provided, return all columns, except for the OBSERVED_AT_FEATURE
            # (the REPLACED_OBSERVED_AT was already dropped in _decode_col_names)
            for x in df.columns:
                if x not in expected_cols and not x.startswith(f"{PSEUDONAMESPACE}.") and "chalk_observed_at" not in x:
                    expected_cols[x] = pl.col(x)

        else:
            # Make a best-effort attempt to determine the pkey and ts column fqn from the root namespace
            # of the other features
            root_ns = get_unique_item(
                [x.split(".")[0] for x in df.columns if not x.startswith(f"{PSEUDONAMESPACE}.")], "root_ns"
            )
            ts_feature = None
            pkey_feature = None
            features_cls = None
            if root_ns in FeatureSetBase.registry:
                features_cls = FeatureSetBase.registry[root_ns]
                ts_feature = features_cls.__chalk_ts__
                pkey_feature = features_cls.__chalk_primary__
            for x in output_feature_fqns:
                if features_cls is not None and x in [f.fqn for f in features_cls.features if f.is_has_one]:
                    for col in df.columns:
                        if col.startswith(f"{x}.") and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x == root_ns:
                    for col in df.columns:
                        if col.startswith(root_ns) and not col.startswith("__"):
                            expected_cols[col] = pl.col(col)
                    continue
                if x in expected_cols:
                    continue
                if x in df.columns:
                    if x == str(CHALK_TS_FEATURE):
                        expected_cols[x] = ts_col.alias(x)
                    else:
                        expected_cols[x] = pl.col(x)
                    continue
                if x == str(CHALK_TS_FEATURE) or (ts_feature is not None and x == str(ts_feature)):
                    # The ts feature wasn't returned as the ts feature, but we are able to figure it out from the graph
                    # Alias the ts_col as the ts fqn (or CHALK_TS_FEATURE fqn if that's what was passed in)
                    expected_cols[x] = ts_col.alias(x)
                    continue
                if pkey_feature is not None and x == str(pkey_feature):
                    expected_cols[x] = id_col.alias(x)
                    continue
                else:
                    # We should _never_ hit this as the query should have failed before results are returned
                    # if an invalid feature was requested
                    raise ValueError(f"Feature '{x}' was not found in the results.")

        df = df.select(list(expected_cols.values()))

    elif version == DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1:
        unique_features = set(df.select(pl.col("feature_name").unique())["feature_name"].to_list())
        cols = [
            pl.col("value").filter(pl.col("feature_name") == fqn).first().alias(cast(str, fqn))
            for fqn in unique_features
        ]

        df = df.groupby("pkey").agg(cols)
        decoded_stmts = []
        for col in df.columns:
            if col == "pkey":
                continue
            else:
                decoded_stmts.append(
                    pl.col(col).apply(_json_decode, return_dtype=Feature.from_root_fqn(col).converter.polars_dtype)
                )
        df = df.select(decoded_stmts)
        # it might be a good idea to remember that we used to rename this __id__ column to the primary key
        # We also need to remove columns like feature.__oat__ and feature.__rat__
        df = df.select([col for col in df.columns if not col.endswith("__")])
        return df.select(sorted(df.columns))
    elif version != DatasetVersion.DATASET_WRITER:
        raise ValueError(f"Unsupported version: {version}")

    decoded_stmts = []
    for col, dtype in zip(df.columns, df.dtypes):
        if version in (
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
            DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        ):
            # The parquet file is all JSON-encoded except for the ts column. That is, the only datetime column is for the timestamp,
            # and all other columns are strings
            if isinstance(dtype, pl.Datetime):
                # Assuming that the only datetime column is for timestamps
                decoded_stmts.append(pl.col(col).dt.with_time_zone("UTC"))
            else:
                decoded_stmts.append(pl.col(col).apply(_json_decode))
        elif version == DatasetVersion.NATIVE_DTYPES:
            if column_metadata is None:
                raise ValueError("The columns must be provided if the dataset type is NATIVE_DTYPES")
            # We already decoded the column names so matching against the fqn
            col_metadata = get_unique_item((x for x in column_metadata if x.feature_fqn == col), f"column {col}")
            polars_dtype = pyarrow_to_polars(deserialize_dtype(col_metadata.dtype), col)
            # Don't attempt to cast list and struct types -- it probably won't work
            # Instead, we should load the dataset via pyarrow, rather than via polars
            col_expr = pl.col(col)
            if dtype != polars_dtype and not isinstance(polars_dtype, (pl.Struct, pl.List)):
                col_expr = col_expr.cast(polars_dtype, strict=True)
            decoded_stmts.append(col_expr)
        else:
            raise ValueError(f"Unsupported version: {version}")
    return df.select(decoded_stmts)


def load_dataset(
    uris: List[str],
    version: Union[DatasetVersion, int],
    output_features: Optional[Sequence[Union[str, Feature, FeatureWrapper, Any]]] = None,
    output_id: bool = True,
    output_ts: bool = True,
    executor: Optional[ThreadPoolExecutor] = None,
    lazy: bool = False,
    columns: Optional[Sequence[ColumnMetadata]] = None,
) -> Union[pl.DataFrame, pl.LazyFrame]:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    del pl  # Unused
    if not isinstance(version, DatasetVersion):
        try:
            version = DatasetVersion(version)
        except ValueError:
            raise ValueError(
                (
                    f"The dataset version ({version}) is not supported by this installed version of the Chalk client. "
                    "Please upgrade your chalk client and try again."
                )
            )
    if version == DatasetVersion.DATASET_WRITER:
        return _load_dataset_from_chalk_writer(uris)
    output_feature_fqns = (
        None
        if output_features is None
        else [x if isinstance(x, str) else ensure_feature(x).root_fqn for x in output_features]
    )
    if version in (
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
        DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2,
        DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1,
        DatasetVersion.NATIVE_DTYPES,
    ):
        return _load_dataset_bigquery(
            uris,
            executor,
            version=version,
            output_feature_fqns=output_feature_fqns,
            output_id=output_id,
            output_ts=output_ts,
            lazy=lazy,
            columns=columns,
        )
    assert_never(version)
