from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence, Tuple


class ValueType(str, Enum):
    """Specifies supported value types supported by Variables."""

    REAL = "real"
    SIGMOID = "sigmoid"
    PROBABILITY = "probability"  # single probability
    PROBABILITY_SAMPLE = "probability_sample"  # sample from single probability
    PROBABILITY_DISTRIBUTION = (
        "probability_distribution"  # probability distribution over classes
    )
    CLASS = "class"  # sample from probability distribution over classes


@dataclass
class _Variable:
    name: str
    value_range: Tuple[Any, Any]
    units: str
    type: ValueType
    variable_label: str
    rescale: float
    is_covariate: bool


@dataclass
class Variable(_Variable):
    """Describes an experimental variable: name, type, range, units, and value of a variable."""

    name: str = ""
    value_range: Tuple[Any, Any] = (0, 1)
    units: str = ""
    type: ValueType = ValueType.REAL
    variable_label: str = ""
    rescale: float = 1
    is_covariate: bool = False


@dataclass
class IV(Variable):
    """Independent variable."""

    name: str = "IV"
    variable_label: str = "Independent Variable"


@dataclass
class DV(Variable):
    """Dependent variable."""

    name: str = "DV"
    variable_label: str = "Dependent Variable"


@dataclass(frozen=True)
class VariableCollection:
    """Immutable metadata about dependent / independent variables and covariates."""

    independent_variables: Sequence[Variable] = field(default_factory=list)
    dependent_variables: Sequence[Variable] = field(default_factory=list)
    covariates: Sequence[Variable] = field(default_factory=list)


@dataclass
class IVTrial(IV):
    """
    Experiment trial as independent variable.
    """

    name: str = "trial"
    UID: str = ""
    variable_label: str = "Trial"
    units: str = "trials"
    priority: int = 0
    value_range: Tuple[Any, Any] = (0, 10000000)
    value: float = 0
