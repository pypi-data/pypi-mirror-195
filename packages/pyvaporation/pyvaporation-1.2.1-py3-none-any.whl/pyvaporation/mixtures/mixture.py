import typing

import attr
import numpy

from ..components import Component
from ..utils import NRTLParameters, R, UNIQUACParameters


def _is_in_0_to_1_range(instance: typing.Any, attribute, value: float) -> None:
    if not 0 <= value <= 1:
        raise ValueError("Give %s value is not in [0, 1] range" % value)


class CompositionType:
    """
    A class to describe type of the composition
    """

    molar: str = "molar"
    weight: str = "weight"


@attr.s(auto_attribs=True)
class Mixture:
    """
    A class to represent mixtures
    """

    name: str
    first_component: Component
    second_component: Component
    nrtl_params: typing.Optional[NRTLParameters] = None
    uniquac_params: typing.Optional[UNIQUACParameters] = None

    def __attrs_post_init__(self):
        if self.nrtl_params is None and self.uniquac_params is None:
            raise ValueError(
                "Component Interaction parameters are required to create a mixture!"
            )


class ActivityCoefficientModel:
    """
    Class to represent types of activity coefficient model used for calculation of partial pressures
    """

    NRTL: str = "NRTL"
    UNIQUAC: str = "UNIQUAC"


@attr.s(auto_attribs=True)
class Composition:
    """
    A class to represent composition of the mixtures
    """

    p: float = attr.ib(validator=_is_in_0_to_1_range)
    type: str

    @property
    def first(self) -> float:
        """
        Returns fraction of the first test_components
        """
        return self.p

    @property
    def second(self) -> float:
        """
        Returns fraction of the second test_components
        """
        return 1 - self.p

    def to_molar(self, mixture: Mixture) -> "Composition":
        """
        Converts Composition to molar %
        """
        if self.type == CompositionType.molar:
            return self
        else:
            p = (self.p / mixture.first_component.molecular_weight) / (
                self.p / mixture.first_component.molecular_weight
                + (1 - self.p) / mixture.second_component.molecular_weight
            )
            return Composition(p=p, type=CompositionType.molar)

    def to_weight(self, mixture: Mixture) -> "Composition":
        """
        Converts Composition to weight %
        """
        if self.type == CompositionType.weight:
            return self
        else:
            p = (mixture.first_component.molecular_weight * self.p) / (
                mixture.first_component.molecular_weight * self.p
                + mixture.second_component.molecular_weight * (1 - self.p)
            )
            return Composition(p=p, type=CompositionType.weight)


def get_partial_pressures(
    temperature: float,
    mixture: Mixture,
    composition: Composition,
    calculation_type: str = ActivityCoefficientModel.NRTL,
) -> typing.Tuple[float, float]:
    """
    Calculation of partial pressures of both test_components
    :params
    temperature: temperature in K
    mixture: a mixture for which the calculation should be conducted
    composition: specified composition in mol or weight %
    :return: Partial pressures as a tuple, test_components wise in kPa
    """
    if composition.type == CompositionType.weight:
        composition = composition.to_molar(mixture=mixture)

    activity_coefficients = calculate_activity_coefficients(temperature=temperature,
                                                            mixture=mixture,
                                                            composition=composition,
                                                            calculation_type=calculation_type)
    return (
        mixture.first_component.get_vapor_pressure(temperature)
        * activity_coefficients[0]
        * composition.first,
        mixture.second_component.get_vapor_pressure(temperature)
        * activity_coefficients[1]
        * composition.second,
    )


def calculate_activity_coefficients(
    temperature: float,
    mixture: Mixture,
    composition: Composition,
    calculation_type: str = ActivityCoefficientModel.NRTL,
) -> typing.Tuple[float, float]:
    """
       Calculation of activity coefficients of both test_components
       :params
       temperature: temperature in K
       mixture: a mixture for which the calculation should be conducted
       composition: specified composition in mol or weight %
       :return: activity coefficients as a tuple
       """
    if composition.type == CompositionType.weight:
        composition = composition.to_molar(mixture=mixture)

    if calculation_type == ActivityCoefficientModel.NRTL:

        if mixture.nrtl_params is None:
            raise ValueError("NRTL Parameters must be specified for this type of calculation")

        tau = numpy.array(
            [
                (mixture.nrtl_params.a12 + mixture.nrtl_params.g12 / (R * temperature)),
                (mixture.nrtl_params.a21 + mixture.nrtl_params.g21 / (R * temperature)),
            ]
        )
        if mixture.nrtl_params.alpha21 is None:
            alphas = mixture.nrtl_params.alpha12
        else:
            alphas = [mixture.nrtl_params.alpha12, mixture.nrtl_params.alpha21]

        g_exp = numpy.exp(numpy.multiply(-tau, alphas))

        activity_coefficients = (
            numpy.exp(
                (composition.second**2)
                * (
                    tau[1]
                    * (g_exp[1] / (composition.first + composition.second * g_exp[1]))
                    ** 2
                    + tau[0]
                    * g_exp[0]
                    / (composition.second + composition.first * g_exp[0]) ** 2
                )
            ),
            numpy.exp(
                (composition.first**2)
                * (
                    tau[0]
                    * (g_exp[0] / (composition.second + composition.first * g_exp[0]))
                    ** 2
                    + tau[1]
                    * g_exp[1]
                    / (composition.first + composition.second * g_exp[1]) ** 2
                )
            ),
        )

        return activity_coefficients

    elif calculation_type == ActivityCoefficientModel.UNIQUAC:
        # The implementation is based on https://doi.org/10.1021/i260068a028
        if composition.first == 0:
            composition = Composition(p=0.00001, type="molar")
        if composition.second == 0:
            composition = Composition(p=0.99999, type="molar")

        if mixture.uniquac_params is None:
            raise ValueError("UNIQUAC Parameters must be specified for this type of calculation")
        if mixture.first_component.uniquac_constants is None or mixture.second_component.uniquac_constants is None:
            raise ValueError("UNIQUAC Constants for all Components must be specified for this type of calculation")

        phi_sum = (
            composition.first * mixture.first_component.uniquac_constants.r
            + composition.second * mixture.second_component.uniquac_constants.r
        )
        phi_1 = (
            composition.first * mixture.first_component.uniquac_constants.r / phi_sum
        )
        phi_2 = (
            composition.second * mixture.second_component.uniquac_constants.r / phi_sum
        )

        theta_sum_geometric = (
            composition.first * mixture.first_component.uniquac_constants.q_geometric
            + composition.second
            * mixture.second_component.uniquac_constants.q_geometric
        )

        theta_1_geometric = (
            composition.first
            * mixture.first_component.uniquac_constants.q_geometric
            / theta_sum_geometric
        )
        theta_2_geometric = (
            composition.second
            * mixture.second_component.uniquac_constants.q_geometric
            / theta_sum_geometric
        )

        theta_sum_interaction = (
            composition.first * mixture.first_component.uniquac_constants.q_interaction
            + composition.second
            * mixture.second_component.uniquac_constants.q_interaction
        )

        theta_1_interaction = (
            composition.first
            * mixture.first_component.uniquac_constants.q_interaction
            / theta_sum_interaction
        )
        theta_2_interaction = (
            composition.second
            * mixture.second_component.uniquac_constants.q_interaction
            / theta_sum_interaction
        )

        l_1 = mixture.uniquac_params.z / 2 * (
            mixture.first_component.uniquac_constants.r
            - mixture.first_component.uniquac_constants.q_geometric
        ) - (mixture.first_component.uniquac_constants.r - 1)

        l_2 = mixture.uniquac_params.z / 2 * (
            mixture.second_component.uniquac_constants.r
            - mixture.second_component.uniquac_constants.q_geometric
        ) - (mixture.second_component.uniquac_constants.r - 1)

        a_12 = mixture.uniquac_params.alpha_12 + mixture.uniquac_params.beta_12/temperature
        a_21 = mixture.uniquac_params.alpha_21 + mixture.uniquac_params.beta_21/temperature

        tau_12 = numpy.exp(-a_12/temperature)
        tau_21 = numpy.exp(-a_21/temperature)

        gamma_1 = numpy.exp(
            numpy.log(phi_1 / composition.first)
            + mixture.uniquac_params.z
            / 2
            * mixture.first_component.uniquac_constants.q_geometric
            * numpy.log(theta_1_geometric / phi_1)
            + phi_2
            * (
                l_1
                - mixture.first_component.uniquac_constants.r
                / mixture.second_component.uniquac_constants.r
                * l_2
            ) - mixture.first_component.uniquac_constants.q_interaction
            * numpy.log(theta_1_interaction + theta_2_interaction * tau_21)
            + theta_2_interaction * mixture.first_component.uniquac_constants.q_interaction
            * (tau_21 / (theta_1_interaction+theta_2_interaction * tau_21)
               - tau_12 / (theta_2_interaction + theta_1_interaction * tau_12))
        )

        gamma_2 = numpy.exp(
            numpy.log(phi_2 / composition.second)
            + mixture.uniquac_params.z
            / 2
            * mixture.second_component.uniquac_constants.q_geometric
            * numpy.log(theta_2_geometric / phi_2)
            + phi_1
            * (
                    l_2
                    - mixture.second_component.uniquac_constants.r
                    / mixture.first_component.uniquac_constants.r
                    * l_1
            ) - mixture.second_component.uniquac_constants.q_interaction
            * numpy.log(theta_2_interaction + theta_1_interaction * tau_12)
            + theta_1_interaction * mixture.second_component.uniquac_constants.q_interaction
            * (tau_12 / (theta_2_interaction + theta_1_interaction * tau_21)
               - tau_12 / (theta_1_interaction + theta_2_interaction * tau_12))
        )

        return gamma_1, gamma_2
