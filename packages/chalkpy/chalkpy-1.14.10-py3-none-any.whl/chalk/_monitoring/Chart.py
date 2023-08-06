import dataclasses
import zlib
from copy import deepcopy
from typing import Any, Callable, ClassVar, List, Literal, Optional, Set, Tuple, TypeVar, Union, overload

from typing_extensions import ParamSpec

from chalk._monitoring.charts_codegen import Series
from chalk._monitoring.charts_enums_codegen import (
    AlertSeverityKind,
    ChartLinkKind,
    MetricFormulaKind,
    ThresholdPosition,
)
from chalk._monitoring.charts_series_base import SeriesBase, ThresholdFunction
from chalk.features import FeatureWrapper
from chalk.features.resolver import Resolver, ResolverProtocol
from chalk.utils.duration import parse_chalk_duration


@dataclasses.dataclass
class _SingleSeriesOperand:
    operand: int


@dataclasses.dataclass
class _MultiSeriesOperand:
    operands: List[int]


@dataclasses.dataclass
class _DatasetFeatureOperand:
    dataset: str
    feature: str


class _Formula:
    def __init__(
        self,
        name: Optional[str] = None,
        kind: Optional[Union[MetricFormulaKind, str]] = None,
        operands: Optional[Union[_SingleSeriesOperand, _MultiSeriesOperand, _DatasetFeatureOperand]] = None,
    ):
        self._name = name
        self._kind = MetricFormulaKind(kind.upper()) if kind else None
        self._operands = operands

    def with_name(self, name: str) -> "_Formula":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_kind(self, kind: Union[MetricFormulaKind, str]) -> "_Formula":
        copy = self._copy_with()
        copy._kind = MetricFormulaKind(kind.upper())
        return copy

    def with_operands(
        self, operands: Union[_SingleSeriesOperand, _MultiSeriesOperand, _DatasetFeatureOperand]
    ) -> "_Formula":
        copy = self._copy_with()
        copy._operands = operands
        return copy

    def _copy_with(self) -> "_Formula":
        self_copy = deepcopy(self)
        return self_copy

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        kind = str(self._kind) if self._kind else "."
        operands = ""
        if isinstance(self._operands, _SingleSeriesOperand):
            operands = self._operands.operand
        elif isinstance(self._operands, _MultiSeriesOperand):
            operands = self._operands.operands
        elif isinstance(self._operands, _DatasetFeatureOperand):
            operands = f"{self._operands.dataset}.{self._operands.feature}"

        formula_string = f"formula.{name}.{kind}.{operands}"

        return zlib.crc32(formula_string.encode())


class Trigger:
    """
    Class to attach an alert to a Chart. Usually instantiated with the `Chart(...).with_trigger(Trigger(...))` method.
    """

    def __init__(
        self,
        name: str,
        severity: Optional[
            Literal[
                "CRITICAL",
                "ERROR",
                "WARNING",
                "INFO",
            ]
        ] = None,
        threshold_position: Optional[Union[ThresholdPosition, str]] = None,
        threshold_value: Optional[float] = None,
        series_name: Optional[str] = None,
        channel_name: Optional[str] = None,
    ):
        self._name = name
        self._severity = severity and AlertSeverityKind(severity.upper())
        self._threshold_position = threshold_position
        self._threshold_value = threshold_value
        self._series_name = series_name
        self._channel_name = channel_name

    def with_name(self, name: str) -> "Trigger":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_severity(
        self,
        severity: Literal[
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
        ],
    ) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind(severity.upper())
        return copy

    def with_critical_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.CRITICAL
        return copy

    def with_error_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.ERROR
        return copy

    def with_warning_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.WARNING
        return copy

    def with_info_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.INFO
        return copy

    def with_threshold_position(self, threshold_position: Union[ThresholdPosition, str]) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_position = ThresholdPosition(threshold_position.upper())
        return copy

    def with_threshold_value(self, threshold_value: float) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_value = threshold_value
        return copy

    def with_series_name(self, series_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._series_name = series_name
        return copy

    def with_channel_name(self, channel_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._channel_name = channel_name
        return copy

    def _copy_with(self) -> "Trigger":
        self_copy = deepcopy(self)
        return self_copy

    def __str__(self) -> str:
        return f"Trigger(name='{self._name}')"

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        severity = str(self._severity) if self._severity else "."
        threshold_position = str(self._threshold_position) if self._threshold_position else "."
        threshold_value = str(self._threshold_value) if self._threshold_value else "."
        series_name = self._series_name if self._series_name else "."
        channel_name = self._channel_name if self._channel_name else "."

        trigger_string = (
            f"trigger.{name}.{severity}.{threshold_position}." f"{threshold_value}.{series_name}.{channel_name}"
        )

        return zlib.crc32(trigger_string.encode())


P = ParamSpec("P")
T = TypeVar("T")


def _copy_with(function: Callable[P, "Chart"]) -> Callable[P, "Chart"]:
    def inner(self, *args, **kwargs):
        copy = deepcopy(self)
        if not self._keep:
            if self in Chart._registry:
                Chart._registry.remove(self)
        return_copy = function(copy, *args, **kwargs)
        Chart._registry.add(return_copy)
        return return_copy

    return inner


# MetricConfigGQL
class Chart:
    """
    Class describing a single visual metric.
    """

    _registry: ClassVar[Set[Union[str, "Chart"]]] = set()

    def __init__(self, name: str, window_period: str = "1h", keep: Optional[bool] = False):
        """

        Parameters
        ----------
        name
            The name of the chart
        window_period
            The length of the window, e.g. "20m" or "1h"
        keep
            By default, the builder methods that return Charts make a deepcopy
            and be deregistered from deployment. If `keep=True`, this chart
            and all descendant charts will be registered automatically.

        Returns
        -------
        Chart
            Your first instance of a Chart!
        """
        self._name = name
        self._window_period = window_period
        self._series: List[SeriesBase] = []
        self._formulas: List[_Formula] = []
        self._trigger = None
        self._keep = keep
        self._entity_id = None
        self._entity_kind = ChartLinkKind.manual
        Chart._registry.add(self)

    @_copy_with
    def with_name(self, name: str) -> "Chart":
        """Override the name of a chart.

        Parameters
        ----------
        name
            A new name for a chart.

        Returns
        -------
        Chart
            A copy of your chart with the new name
        """
        self._name = name
        return self

    @_copy_with
    def with_window_period(self, window_period: str) -> "Chart":
        """Change the window period for a chart.

        Parameters
        ----------
        window_period
            A new window period for a chart, e.g. "20m" or "1h".

        Returns
        -------
        Chart
            A copy of your chart with the new window period
        """
        parse_chalk_duration(window_period)
        self._window_period = window_period
        return self

    @_copy_with
    def with_series(self, series: SeriesBase) -> "Chart":
        """Attaches a `Series` to your `Chart` instance.

        Parameters
        ----------
        series
            A Series instance to attach to the Chart.
            A Chart can have any number of Series.

        Returns
        -------
        Chart
            A copy of your chart with the new name
        """
        if not isinstance(series, SeriesBase):
            raise ValueError(f"'series' value '{series}' must be a Series object")
        self._series.append(series)
        if series._entity_id:
            self._entity_id = series._entity_id
            self._entity_kind = series._entity_kind
        return self

    def get_series(self, series_name: str) -> SeriesBase:
        """Get a `Series` from your `Chart` by series name.

        It is advised to use different series names within your charts.

        Parameters
        ----------
        series_name
            The name of the Series

        Returns
        -------
        Series
            The first series added to your `Chart` with the given series name.
        """
        for series in self._series:
            if series._name == series_name:
                return series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    def _get_series_index(self, series_name: str) -> Tuple[int, SeriesBase]:
        for i, series in enumerate(self._series):
            if series._name == series_name:
                return i, series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    @overload
    def with_formula(self, /, formula: _Formula, **kwargs) -> "Chart":
        ...

    @overload
    def with_formula(self, /, name: str, **kwargs) -> "Chart":
        ...

    @_copy_with
    def with_formula(self, /, name: Optional[str] = None, formula: Optional[_Formula] = None, **kwargs) -> "Chart":
        if formula:
            if not isinstance(formula, _Formula):
                raise ValueError(f"'formula' value '{formula}' must be a Formula object")
            self._formulas.append(formula)
            return self
        if name:
            if not isinstance(name, str):
                raise ValueError(f"'name' value '{name}' must be a string")
            new_formula = _Formula(**kwargs)
            self._formulas.append(new_formula)
            return self
        raise ValueError("Either a 'name' for a new formula or an existing Formula 'formula' must be supplied")

    @_copy_with
    def with_trigger(
        self,
        expression: ThresholdFunction,
        trigger_name: str,
        severity: Optional[Union[AlertSeverityKind, str]] = None,
        channel_name: Optional[str] = None,
    ) -> "Chart":
        """Attaches a `Trigger` to your `Chart`. Your `Chart` may optionally have one `Trigger`.

        Parameters
        ----------
        expression
            Triggers are applied when a certain series is above or below a given value.
            The expression specifies the series, operand, and value as follows
                - the left-hand side of the expression must be a Series instance.
                - the operand must be `<` or `>`
                - the right-hand side must be an `int` or `float`
            Thus, if we have a Series instance `series1`, `expression=series1 > 0.5`
            will result in an alert when `series` is greater than 0.5.
        trigger_name
            The name for the new trigger.
        severity
            The severity of the trigger.
                - `critical`
                - `error`
                - `warning`
                - `info`
        channel_name
            The owner or email of the trigger.

        Returns
        -------
        Chart
            A copy of your chart with the new trigger.
        """
        if not isinstance(expression.lhs, SeriesBase):
            raise ValueError(f"Left hand side of expression '{expression.lhs}' must be a Series")
        threshold_position = ThresholdPosition.ABOVE if expression.operation == ">" else ThresholdPosition.BELOW
        trigger = Trigger(
            name=trigger_name,
            severity=AlertSeverityKind(severity.upper()),
            threshold_position=threshold_position,
            threshold_value=expression.rhs,
            series_name=expression.lhs._name,
            channel_name=channel_name,
        )
        self._trigger = trigger
        return self

    @_copy_with
    def with_feature_link(self, feature: Any) -> "Chart":
        """Explicitly link a Chart to a feature.
        This chart will then be visible on the webpage for this feature.
        Charts may only be linked to one entity.

        Parameters
        ----------
        feature
            A Chalk feature

        Returns
        -------
        Chart
            A copy of your chart linked to the feature.
        """
        self._entity_kind = ChartLinkKind.feature
        self._entity_id = str(feature) if isinstance(feature, FeatureWrapper) else feature
        return self

    @_copy_with
    def with_resolver_link(self, resolver: ResolverProtocol) -> "Chart":
        """Explicitly link a chart to a resolver.
        This chart will then be visible on the webpage for this resolver.
        Charts may only be linked to one entity.

        Parameters
        ----------
        resolver
            A Chalk resolver

        Returns
        -------
        Chart
            A copy of your chart linked to the resolver.
        """
        self._entity_kind = ChartLinkKind.resolver
        self._entity_id = resolver.fqn if isinstance(resolver, Resolver) else resolver
        return self

    @_copy_with
    def with_query_link(self, query_name: str) -> "Chart":
        """Explicitly link a chart to a query.
        This chart will then be visible on the webpage for this query.
        Charts may only be linked to one entity.

        Parameters
        ----------
        query_name
            A name of a Chalk query

        Returns
        -------
        Chart
            A copy of your chart linked to the query.
        """
        self._entity_kind = ChartLinkKind.query
        self._entity_id = query_name
        return self

    def keep(self) -> "Chart":
        """Designates that this chart and all of its descendants will be registered.

        Returns
        -------
        Chart
            The same chart.
        """
        self._keep = True
        return self

    def __str__(self) -> str:
        return f"Chart(name='{self._name}')"

    def __getitem__(self, key: str) -> Union[SeriesBase, _Formula]:
        """Retrieve a series or formula by name from a chart

        Parameters
        ----------
        key
            The name of the series or formula to retrieve.

        Returns
        -------
        The series or formula with the given name.

        """
        for series in self._series:
            if series._name == key:
                return series
        for formula in self._formulas:
            if formula._name == key:
                return formula
        raise ValueError(f"No series or formula named '{key}' exists in Chart {self._name}")

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def __hash__(self):
        name = self._name if self._name else "."

        window_period = self._window_period if self._window_period else "."
        chart_string = f"chart.{name}.{window_period}"

        series_hash = ".".join(sorted([str(hash(series)) for series in self._series]))
        formulas = ".".join(sorted([str(hash(formula)) for formula in self._formulas]))
        trigger = str(hash(self._trigger)) if self._trigger else "."

        return zlib.crc32(chart_string.encode() + series_hash.encode() + formulas.encode() + trigger.encode())
