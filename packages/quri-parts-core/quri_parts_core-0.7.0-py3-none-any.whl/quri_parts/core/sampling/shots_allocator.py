# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from collections.abc import Collection

from numpy.random import default_rng

from quri_parts.core.operator import CommutablePauliSet, Operator
from quri_parts.core.sampling import PauliSamplingSetting, PauliSamplingShotsAllocator


def _rounddown_to_unit(n: float, shot_unit: int) -> int:
    return shot_unit * math.floor(n / shot_unit)


def _abs_sum_of_pauli_coeff(op: Operator, pauli_set: CommutablePauliSet) -> float:
    return sum([abs(op[pauli_label]) ** 2 for pauli_label in pauli_set])


def _calc_ratios(
    operator: Operator, pauli_sets: Collection[CommutablePauliSet]
) -> list[float]:
    weights = [
        math.sqrt(_abs_sum_of_pauli_coeff(operator, pauli_set))
        for pauli_set in pauli_sets
    ]
    weights_sum = sum(weights)
    return list(map(lambda w: w / weights_sum, weights))


def create_equipartition_shots_allocator(
    shot_unit: int = 1,
) -> PauliSamplingShotsAllocator:
    """Returns a :class:`~PauliSamplingShotsAllocator` that distributes the
    number of shots equally among the groups.

    Args:
        shot_unit: Unit of shot counts. Each distributed number of shots is
            rounded down to the nearest multiple of this number. (default: 1)

    Note:
        The sum of allocated shots may be less than `total_shots` due to the rounding.
    """

    def allocator(
        operator: Operator,
        pauli_sets: Collection[CommutablePauliSet],
        total_shots: int,
    ) -> Collection[PauliSamplingSetting]:

        n_terms = len(pauli_sets)
        shots_per_term = _rounddown_to_unit(total_shots / n_terms, shot_unit)
        return frozenset(
            {
                PauliSamplingSetting(
                    pauli_set=pauli_set,
                    n_shots=shots_per_term,
                )
                for pauli_set in pauli_sets
            }
        )

    return allocator


def create_proportional_shots_allocator(
    shot_unit: int = 1,
) -> PauliSamplingShotsAllocator:
    r"""Returns a :class:`~PauliSamplingShotsAllocator` that distributes the
    number of shots in a way that is proportional to the target coefficient.

    The number of shots for measurement group :math:`i`, :math:`n_i`, is determined by

    .. math::
        n_i = \frac{w_i}{\sum_j w_j}

    where :math:`w_j` is a weight for the :math:`j`-th measurement group that is
    defined by the Euclidean norm of the coefficients among Pauli terms of the
    :math:`j`-th measurement group.

    References:
        D. Wecker, M. B. Hastings, and M. Troyer, Phys. Rev. A 92, 042303 (2015).
        M. Kohda, R. Imai, et al., arXiv:2112.07416 (2021). See Appendix D.

    Args:
        shot_unit: Unit of shot counts. Each distributed number of shots is
            rounded down to the nearest multiple of this number. (default: 1)

    Note:
        The sum of allocated shots may be less than `total_shots` due to the rounding.
    """

    def allocator(
        operator: Operator, pauli_sets: Collection[CommutablePauliSet], total_shots: int
    ) -> Collection[PauliSamplingSetting]:

        pauli_sets = tuple(pauli_sets)  # to fix the order of elements

        ratios = _calc_ratios(operator, pauli_sets)
        shots_list = [
            _rounddown_to_unit(total_shots * ratio, shot_unit) for ratio in ratios
        ]
        return frozenset(
            {
                PauliSamplingSetting(
                    pauli_set=pauli_set,
                    n_shots=n_shots,
                )
                for (pauli_set, n_shots) in zip(pauli_sets, shots_list)
            }
        )

    return allocator


def create_weighted_random_shots_allocator(
    seed: int = 1,
    shot_unit: int = 1,
) -> PauliSamplingShotsAllocator:
    r"""Returns a :class:`~PauliSamplingShotsAllocator` that distributes the
    number of shots by sampling from a multinomial probability distribution
    defined by the target coefficients. The probability is determined by eq.
    (10) in the reference below.

    References:
        Operator Sampling for Shot-frugal Optimization in Variational Algorithms
        Andrew Arrasmith, Lukasz Cincio, Rolando D. Somma, and Patrick J. Coles,
        arXiv:2004.06252 (2020)

    Args:
        seed: Seed used to initialize NumPy's default_rng.
        shot_unit: Unit of shot counts. Each distributed number of shots is
            multiple of this number. (default: 1)

    Note:
        If `shot_unit` is greater than 1, the quotient `total_shots // shot_unit` is
        once distributed to each group by multinomial distribution, and then each of
        them is multiplied by `shot_unit`.
        In this case, the sum of allocated shots may be less than `total_shots`.
    """
    rng = default_rng(seed)

    def allocator(
        operator: Operator, pauli_sets: Collection[CommutablePauliSet], total_shots: int
    ) -> Collection[PauliSamplingSetting]:
        pauli_sets = tuple(pauli_sets)  # to fix the order of elements

        ratios = _calc_ratios(operator, pauli_sets)
        total_shots_per_shot_unit = total_shots // shot_unit
        shots_per_shot_unit = rng.multinomial(
            total_shots_per_shot_unit, ratios, size=1
        )[0]
        shots_list = (shot_unit * shots_per_shot_unit).tolist()
        return frozenset(
            {
                PauliSamplingSetting(
                    pauli_set=pauli_set,
                    n_shots=n_shots,
                )
                for (pauli_set, n_shots) in zip(pauli_sets, shots_list)
            }
        )

    return allocator
