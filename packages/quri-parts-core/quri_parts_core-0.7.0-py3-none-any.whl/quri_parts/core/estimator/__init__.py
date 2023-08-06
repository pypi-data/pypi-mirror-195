# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import abstractproperty
from collections.abc import Iterable, Sequence
from typing import Callable, Optional, Protocol, TypeVar, Union, cast, overload

from typing_extensions import TypeAlias

from quri_parts.core.operator import Operator, PauliLabel
from quri_parts.core.state import (
    CircuitQuantumState,
    ParametricCircuitQuantumState,
    ParametricQuantumStateVector,
    QuantumStateVector,
)

EstimateValue = TypeVar("EstimateValue", float, complex, covariant=True)


class Estimate(Protocol[EstimateValue]):
    """Estimate is an interface for classes representing an estimate for a
    certain quantity.

    This interface only contains read-only properties, so an
    implementation can be a (frozen) dataclass or a namedtuple.
    """

    @abstractproperty
    def value(self) -> EstimateValue:
        """The estimate (estimated value) itself."""
        ...

    @abstractproperty
    def error(self) -> float:
        """Represents the \"error\" of the estimate.

        The precise meaning of the \"error\" depends on what type the
        estimate is. If the estimate is a sample mean calculated by
        sampling from some sample distribution, the error is the
        standard error calculated from the samples. If the estimate is
        an exact value calculated without sampling, the error is zero.
        """
        ...


class Estimates(Protocol[EstimateValue]):
    """Estimates is an interface for classes representing estimates for a
    certain quantity.

    This interface only contains read-only properties, so an
    implementation can be a (frozen) dataclass or a namedtuple.
    """

    @abstractproperty
    def values(self) -> Sequence[EstimateValue]:
        """The estimates (estimated values) themselves."""
        ...

    @abstractproperty
    def error_matrix(self) -> Optional[Sequence[Sequence[float]]]:
        """Represents the \"error\" of estimate values.

        The precise meaning of the \"error\" depends on what type the
        estimate is. Basically, if we can get N estimate values, this
        will return N x N covariance matrix.
        """
        ...


#: (Concurrent)QuantumEstimator accepts a single :class:`~PauliLabel` as well as an
#: :class:`~Operator`. Here we call them an "Estimatable".
Estimatable: TypeAlias = Union[Operator, PauliLabel]

#: A type variable represents *any* non-parametric quantum state classes.
#: This is different from :class:`quri_parts.core.state.QuantumStateT`;
#: ``QuantumStateT`` represents *either one of* the classes, while ``_StateT`` also
#: covers *a union of* multiple state classes.
_StateT = TypeVar("_StateT", bound=Union[CircuitQuantumState, QuantumStateVector])

#: QuantumEstimator represents a function that estimates an expectation value of
#: a given :class:`~Operator` for a given non-parametric state.
#: It theoretically corresponds to a value given by sandwiching the operator between
#: a bra and a ket of the state.
#: This is a generic type and you need to specify what kind of state classes
#: it is applicable to.
QuantumEstimator: TypeAlias = Callable[[Estimatable, _StateT], Estimate[complex]]

#: ConcurrentQuantumEstimator represents a function that estimates expectation values of
#: given :class:`~Operator`\ s for given non-parametric states.
#: It basically works in the same way as :class:`~QuantumEstimator`, except that
#: it performs estimation for multiple operators and states concurrently.
#: Numbers of operators and states (i.e. lengths of the first and second arguments)
#: should satisfy one of the followings:
#:
#: * Only one operator is specified.
#: * Only one state is specified.
#: * The number of the operators is the same as the number of the states. In this case,
#:   an operator and a state with the same index are used to estimate one expectation
#:   value.
#:
#: This is a generic type and you need to specify what kind of state classes
#: it is applicable to.
ConcurrentQuantumEstimator: TypeAlias = Callable[
    [Sequence[Estimatable], Sequence[_StateT]],
    Iterable[Estimate[complex]],
]

#: A type variable represents *any* parametric quantum state classes.
#: This is different from :class:`quri_parts.core.state.ParametricQuantumStateT`;
#: ``ParametricQuantumStateT`` represents *either one of* the classes,
#: while ``_ParametricStateT`` also covers *a union of* multiple state classes.
_ParametricStateT = TypeVar(
    "_ParametricStateT",
    bound=Union[ParametricCircuitQuantumState, ParametricQuantumStateVector],
)

#: ParametricQuantumEstimator represents a function that estimates an expectation value
#: of a given :class:`~Operator` for a given parametric state
#: with given parameter values (the third argument).
#: This is a generic type and you need to specify what kind of state classes
#: it is applicable to.
ParametricQuantumEstimator: TypeAlias = Callable[
    [Estimatable, _ParametricStateT, Sequence[float]], Estimate[complex]
]

#: ConcurrentParametricQuantumEstimator represents a function that estimates
# expectation values of a given :class:`~Operator` for a given
# parametric state with multiple sets of parameter values
# (the third argument). It basically works in the same way as
# :class:`~ParametricQuantumEstimator`, except that it performs estimation for multiple
# sets of parameter values concurrently. Length of the returned iterable is the same as
# the number of given parameter sets.
#: This is a generic type and you need to specify what kind of state classes
#: it is applicable to.
ConcurrentParametricQuantumEstimator: TypeAlias = Callable[
    [Estimatable, _ParametricStateT, Sequence[Sequence[float]]],
    Iterable[Estimate[complex]],
]


@overload
def create_parametric_estimator(
    estimator: QuantumEstimator[Union[CircuitQuantumState, QuantumStateVector]],
) -> ParametricQuantumEstimator[
    Union[ParametricCircuitQuantumState, ParametricQuantumStateVector]
]:
    ...


@overload
def create_parametric_estimator(
    estimator: QuantumEstimator[CircuitQuantumState],
) -> ParametricQuantumEstimator[ParametricCircuitQuantumState]:
    ...


@overload
def create_parametric_estimator(
    estimator: QuantumEstimator[QuantumStateVector],
) -> ParametricQuantumEstimator[ParametricQuantumStateVector]:
    ...


def create_parametric_estimator(
    estimator: QuantumEstimator[_StateT],
) -> ParametricQuantumEstimator[_ParametricStateT]:
    """Creates parametric estimator from estimator."""

    def parametric_estimator(
        operator: Estimatable,
        state: _ParametricStateT,
        params: Sequence[float],
    ) -> Estimate[complex]:
        s = cast(_StateT, state.bind_parameters(params))
        return estimator(operator, s)

    return parametric_estimator


#: GradientEstimator represents a function that estimates gradient values
#: of an expectation value of a given :class:`~Operator` for a given parametric state
#: with given parameter values (the third argument).
#: This is a generic type and you need to specify what kind of state classes
#: it is applicable to.
GradientEstimator: TypeAlias = Callable[
    [Estimatable, _ParametricStateT, Sequence[float]],
    Estimates[complex],
]
