from .data_types import *

from math import pow, sqrt


def VogelEquation(p: NUMERIC, p_res: NUMERIC) -> NUMERIC:
    """
    Calculation of flow rate ratio
    Using Vogel Equation

    INPUT:
        p (pressure): numeric
        p_res (reservoir presure): numeric

    OUTPUT: numeric
    """
    pr = p / p_res          # pressure ratio

    # Vogel equation result
    result = 1 - (0.2 * pr) - (0.8 * pow(pr, 2))

    return result if result > 0 else 0.0001


def PressureRatioFromVogelEquation(q: NUMERIC, q_max: NUMERIC):
    """
    Calculation of pressure ratio
    Based on re-arrange of Vogel equation

    INPUT:
        p_res (reservoir pressure): numeric
        q (flow rate): numeric
        q_max (max flow rate): numeric

    OUTPUT: numeric
    """
    # Quadratic equation constants
    a = -0.8
    b = -0.2
    c = 1

    # Flow rate ratio
    qr = q / q_max

    # Analytical results of pressure ratio
    result = (-a - sqrt(pow(b, 2) - (4 * a * (c - qr)), 0.5)) / (2 * a)

    return result


def FetkovichEquation(
    p: NUMERIC, p_res: NUMERIC, C: OPTIONAL_NUMERIC, n: NUMERIC
) -> NUMERIC:
    """
    Calculation of flow rate (q) using Fetkovich equation
    along with Rawlin and Schellhardt method

    INPUT
        p (wellbore pressure): numeric
        p_res (reservoir_pressure): numeric
        C (C coefficient): numeric
        n (n coefficient): numeric

    OUTPUT
        q: numeric
    """

    psr = pow(p / p_res, 2)

    result = pow(1 - psr, n)
    return result


def PressureRatioFromFetkovichEquation(
    q: NUMERIC, q_max: NUMERIC, n: NUMERIC
) -> NUMERIC:
    """
    Calculation of pressure ratio
    Based on re-arrange of Vogel equation

    INPUT:
        p_res (reservoir pressure): numeric
        q (flow rate): numeric
        q_max (max flow rate): numeric

    OUTPUT: numeric
    """
    qr = q / q_max

    pr = sqrt(1 - sqrt(qr, n), 2)

    return pr


def WigginEquation(
        phase: STRING, p: NUMERIC, p_res: NUMERIC
) -> NUMERIC:
    """
    Calculation of flow rate ratio
    using Wiggin equation according to phase selection

    INPUT
        phase: str
        p (wellbore pressure): numeric
        p_res (reservoir pressure): numeric

    OUTPUT
        qr: numeric
    """

    # Initiate pressure ratio
    pr = p / p_res

    # calculation of flow rate ratio
    if (phase == "oil"):
        qr = 1 - (0.52 * pr) - (0.48 * pow(pr, 2))
    elif (phase == "water"):
        qr = 1 - (0.72 * pr) - (0.28 * pow(pr, 2))

    return qr


def PressureRatioFromWigginEquation(phase: STRING, q: NUMERIC, q_max: NUMERIC):
    """
    Calculation of pressure ratio (wellbore pressure)
    Based on re-arrange of Wiggin equation

    INPUT:
        p_res (reservoir pressure): numeric
        q (flow rate): numeric
        q_max (max flow rate): numeric

    OUTPUT: numeric
    """
    # Quadratic equation constants
    a = -0.48 if phase == "oil" else -0.28
    b = -0.52 if phase == "water" else -0.72
    c = 1

    # Flow rate ratio
    qr = q / q_max

    # Analytical results of pressure ratio
    pr = (-a - sqrt(pow(b, 2) - (4 * a * (c - qr)), 0.5)) / (2 * a)

    return pr
