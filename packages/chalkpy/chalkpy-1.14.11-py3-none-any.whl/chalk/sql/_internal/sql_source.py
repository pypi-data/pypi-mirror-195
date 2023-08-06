from __future__ import annotations

import contextlib
import functools
import inspect
import json
import logging
import os
import os.path
import warnings
from dataclasses import dataclass
from os import PathLike
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import pyarrow as pa

from chalk.features import Feature, FeatureConverter, Features, FeatureWrapper, unwrap_feature
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.chalk_query import ChalkQuery
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.string_chalk_query import StringChalkQuery
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, StringChalkQueryProtocol, TableIngestProtocol
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger, get_logging_context
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import URL, Engine
    from sqlalchemy.orm import Session
    from sqlalchemy.sql import Select
    from sqlalchemy.sql.elements import Label
    from sqlalchemy.types import TypeEngine

TTableIngestMixIn = TypeVar("TTableIngestMixIn", bound="TableIngestMixIn")
CHALK_QUERY_LOGGING = env_var_bool("CHALK_QUERY_LOGGING")

_logger = get_logger(__name__)


@dataclass
class TableIngestionPreferences:
    features: Type[Features]
    ignore_columns: Set[str]
    ignore_features: Set[str]
    require_columns: Set[str]
    require_features: Set[str]
    column_to_feature: Dict[str, str]
    cdc: Optional[Union[bool, IncrementalSettings]]


def _force_set_str(x: Optional[List[Any]]) -> Set[str]:
    return set() if x is None else set(map(str, x))


class UnsupportedEfficientExecutionError(ValueError):
    def __init__(self, msg: str, log_level: int) -> None:
        super().__init__(msg)
        self.log_level = log_level


def validate_dtypes_for_efficient_execution(stmt: Select, supported_types: Sequence[Type[TypeEngine]]):
    unsupported_columns = [
        x
        for x in stmt.column_descriptions
        # Using NOT IN rather than not isinstance() as subclasses may override the result processor,
        # which makes it not eligible for efficient execution
        if x["type"].__class__ not in supported_types
    ]
    if len(unsupported_columns) > 0:
        unsupported_columns_and_dtypes = [(x["name"], x["type"].__class__.__name__) for x in unsupported_columns]
        supported_dtypes = [x.__name__ for x in supported_types]
        formatted_supported = ", ".join(supported_dtypes)
        formatted_unsupported = ", ".join([f"{name}({dtype})" for (name, dtype) in unsupported_columns_and_dtypes])
        raise UnsupportedEfficientExecutionError(
            (
                "The SQL statement will be executed into SQLAlchemy objects, as the SQL query returns columns "
                "that cannot be loaded directly into a PyArrow table. For better performance, use only "
                f"the following types in your SQLAlchemy model: {formatted_supported}."
                f"The columns that contain unsupported types are: {formatted_unsupported}."
            ),
            log_level=logging.INFO,
        )


class TableIngestMixIn(TableIngestProtocol):
    ingested_tables: Dict[str, TableIngestionPreferences]

    def with_table(
        self: TTableIngestMixIn,
        *,
        name: str,
        features: Type[Union[Features, Any]],
        ignore_columns: Optional[List[str]] = None,
        ignore_features: Optional[List[Union[str, Any]]] = None,
        require_columns: Optional[List[str]] = None,
        require_features: Optional[List[Union[str, Any]]] = None,
        column_to_feature: Optional[Dict[str, Any]] = None,
        cdc: Optional[Union[bool, IncrementalSettings]] = None,
    ) -> TTableIngestMixIn:
        if name in self.ingested_tables:
            raise ValueError(f"The table {name} is ingested twice.")
        self.ingested_tables[name] = TableIngestionPreferences(
            features=features,
            ignore_columns=_force_set_str(ignore_columns),
            ignore_features=_force_set_str(ignore_features),
            require_columns=_force_set_str(require_columns),
            require_features=_force_set_str(require_features),
            column_to_feature={k: str(v) for k, v in (column_to_feature or {}).items()},
            cdc=cdc,
        )
        return self


class BaseSQLSource(BaseSQLSourceProtocol):
    registry: ClassVar[List["BaseSQLSource"]] = []

    def __init__(self, name: Optional[str]):
        try:
            import sqlalchemy
        except ImportError:
            raise missing_dependency_exception("chalkpy[sql]")
        del sqlalchemy  # unused

        self._incremental_settings = None
        self._resolver_and_sqlfile_to_sqlstring: Dict[Tuple[str, str], str] = {}
        self.registry.append(self)
        self.name = name

    def query_sql_file(
        self,
        path: Union[str, bytes, PathLike],
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, str]] = None,
    ) -> StringChalkQueryProtocol:
        sql_string = None
        fqn = None

        try:
            fqn = get_logging_context().get("labels", {}).get("resolver_fqn")
            if fqn is not None:
                sql_string = self._resolver_and_sqlfile_to_sqlstring.get((fqn, str(path)))
        except Exception:
            pass

        uncached = sql_string is None

        if uncached:
            if os.path.isfile(path):
                with open(path) as f:
                    sql_string = f.read()
            else:
                caller_filename = inspect.stack()[1].filename
                dir_path = os.path.dirname(os.path.realpath(caller_filename))
                if isinstance(path, bytes):
                    path = path.decode("utf-8")
                relative_path = os.path.join(dir_path, path)
                if os.path.isfile(relative_path):
                    with open(relative_path) as f:
                        sql_string = f.read()
        if sql_string is None:
            raise FileNotFoundError(f"No such file: '{str(path)}'")

        if uncached and fqn is not None:
            self._resolver_and_sqlfile_to_sqlstring[(fqn, str(path))] = sql_string

        return self.query_string(
            query=sql_string,
            fields=fields,
            args=args,
        )

    def query_string(
        self,
        query: str,
        fields: Optional[Mapping[str, Union[Feature, Any]]] = None,
        args: Optional[Mapping[str, str]] = None,
    ) -> StringChalkQueryProtocol:
        fields = fields or {}
        fields = {f: unwrap_feature(v) if isinstance(v, FeatureWrapper) else v for (f, v) in fields.items()}
        return StringChalkQuery(source=self, query=query, fields=fields, params=args or {})

    def warm_up(self) -> None:
        from sqlalchemy import text

        with self.get_engine().connect() as cnx:
            cnx.execute(text("select 1"))

    def query(self, *entities: Any) -> ChalkQueryProtocol:
        targets: List[Label] = []
        features: Dict[str, Feature] = {}

        for e in entities:
            if isinstance(e, Features):
                _extract_features(e, e.__chalk_namespace__, targets, features)
            else:
                targets.append(e)

        return ChalkQuery(
            features=features,
            targets=targets,
            source=self,
        )

    def local_engine_url(self) -> URL:
        raise NotImplementedError

    def execute_query(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Any] = None,
    ) -> pa.Table:
        from sqlalchemy.engine import Connection

        try:
            return self.execute_query_efficient(finalized_query, columns_to_converters, connection)
        except NotImplementedError:
            _logger.info(
                (
                    "The SQL statement will be executed into SQLAlchemy objects, as the database backend does "
                    "not support a more efficient execution mechanism."
                )
            )
            pass
        except UnsupportedEfficientExecutionError as e:
            log_level = e.log_level
            _logger.log(log_level, str(e))

        with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
            assert isinstance(cnx, Connection)
            res = cnx.execute(finalized_query.query, finalized_query.params)
            desc = res.cursor.description
            result_columns: list[str] = [col[0] for col in desc]
            converters = columns_to_converters(result_columns)
            data: Dict[str, List[Any]] = {}
            for v in converters.keys():
                # Create an entry for the columns, so the pyarrow table will have the correct columns even
                # if there is no data
                data[v] = []
            for row in res.all():
                for k, v in zip(result_columns, row):
                    if k not in data:
                        # We are not interested in this column
                        continue
                    data[k].append(converters[k].from_rich_to_primitive(v, missing_value_strategy="default_or_allow"))
            # Only keep the columns provided by the schema
            schema = pa.schema([pa.field(k, v.pyarrow_dtype) for (k, v) in converters.items()])
            return pa.Table.from_pydict(data, schema=schema)

    def execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_converters: Callable[[List[str]], Dict[str, FeatureConverter]],
        connection: Optional[Any] = None,
    ) -> pa.Table:
        raise NotImplementedError()

    def compile_query(
        self,
        finalized_query: FinalizedChalkQuery,
        paramstyle: Optional[str] = None,
    ) -> Tuple[str, Sequence[Any], Dict[str, Any]]:
        """Compile a query into a string and the bindparams"""
        dialect = self.local_engine_url().get_dialect()(paramstyle=paramstyle)
        query = finalized_query.query.params(finalized_query.params)
        compiled_query = query.compile(dialect=dialect)
        query_string = compiled_query.string
        return query_string, compiled_query.positiontup or [], compiled_query.params

    def load_env_engine_args(self, name: str) -> Mapping[str, Any]:
        """
        Loads additional engine arguments from env var "{name}_ENGINE_ARGUMENTS"
        """

        extra_args = load_integration_variable(integration_name=name, name="ENGINE_ARGUMENTS")
        if extra_args is None:
            return {}
        else:
            extra_args = json.loads(extra_args)
            assert isinstance(extra_args, dict), "ENGINE_ARGUMENTS must be a JSON object"
            return extra_args

    @functools.lru_cache(None)  # pyright: ignore[reportIncompatibleMethodOverride]
    def get_engine(self, additional_engine_args: Optional[Dict[str, Any]] = None) -> Engine:
        from sqlalchemy.engine import create_engine

        args = self.engine_args()
        if additional_engine_args is not None:
            args.update(additional_engine_args)
        return create_engine(
            url=self.local_engine_url(),
            echo=CHALK_QUERY_LOGGING,
            **args,
        )

    def raw_session(self) -> Session:
        from sqlalchemy.orm import Session

        warnings.warn(
            DeprecationWarning(
                (
                    "The method `raw_session()` is deprecated. Instead, please construct a session directly "
                    "from the underlying engine -- for example:"
                    "`from sqlalchemy.orm import Session; with Session(sql_source.get_engine()) as session: ...`"
                )
            )
        )
        return Session(self.get_engine())


def _extract_features(feature_set: Features, prefix: str, targets: List[Label], features: Dict[str, Feature]):
    import sqlalchemy.sql.functions
    from sqlalchemy import column
    from sqlalchemy.orm import InstrumentedAttribute

    for f in feature_set.features:
        assert f.attribute_name is not None
        try:
            feature_value = getattr(feature_set, f.attribute_name)
        except AttributeError:
            continue
        if f.is_has_many:
            raise ValueError(
                f"Feature '{prefix}.{f.name}' is a nested has-many feature, which is not supported when querying from SQL"
            )
        root_fqn = f"{prefix}.{f.name}"
        if isinstance(feature_value, Features):
            # Nested sub-features
            _extract_features(feature_value, root_fqn, targets, features)
        elif isinstance(feature_value, str):
            # Treat it as a column name
            features[root_fqn] = Feature.from_root_fqn(root_fqn)
            targets.append(column(feature_value).label(root_fqn))
        elif isinstance(feature_value, (sqlalchemy.sql.functions.GenericFunction, InstrumentedAttribute)):
            features[root_fqn] = Feature.from_root_fqn(root_fqn)
            targets.append(feature_value.label(root_fqn))
        else:
            raise TypeError(
                (
                    f"Feature '{root_fqn}' has an unsupported value for SQL queries. "
                    "All values must be a column, a column name string, a nested Features class, or an SQLAlchemy function"
                )
            )
