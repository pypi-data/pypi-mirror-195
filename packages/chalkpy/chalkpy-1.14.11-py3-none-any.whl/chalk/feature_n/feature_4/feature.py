# AUTO-GENERATED FILE.
# Re-run /chalk/feature_n/codegen.py to regenerate contents.
from typing import TypeVar, Generic, Optional, Dict
from chalk.features.dataframe import DataFrameMeta


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")


class Features(Generic[T1, T2, T3, T4]):
    pass


class DataFrame(Generic[T1, T2, T3, T4], metaclass=DataFrameMeta):
    def __getitem__(self, item):
        pass
