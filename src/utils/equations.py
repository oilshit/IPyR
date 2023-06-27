from . import data_types as dt

from math import pow, sqrt

def vogel_equation(p: dt.NUMERIC, p_res: dt.NUMERIC) -> dt.NUMERIC:
    """
    Calculation of flow rate ratio
    Using Vogel Equation

    INPUT:
        p (pressure): dt.NUMERIC
        p_res (reservoir presure): dt.NUMERIC

    OUTPUT: dt.NUMERIC
    """
    pr = p / p_res          # pressure ratio

    # Vogel equation result
    result = 1 - (0.2 * pr) - (0.8 * pow(pr, 2))

    return result if result > 0 else 0.00000001


def pressure_ratio_from_vogel_equation(q: dt.NUMERIC, q_max: dt.NUMERIC):
    """
    Calculation of pressure ratio
    Based on re-arrange of Vogel equation

    INPUT:
        p_res (reservoir pressure): dt.NUMERIC
        q (flow rate): dt.NUMERIC
        q_max (max flow rate): dt.NUMERIC

    OUTPUT: dt.NUMERIC
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


def fetkovich_equation(
    p: dt.NUMERIC, p_res: dt.NUMERIC, C: dt.OPTIONAL_NUMERIC, n: dt.NUMERIC
) -> dt.NUMERIC:
    """
    Calculation of flow rate (q) using Fetkovich equation
    along with Rawlin and Schellhardt method

    INPUT
        p (wellbore pressure): dt.NUMERIC
        p_res (reservoir_pressure): dt.NUMERIC
        C (C coefficient): dt.NUMERIC
        n (n coefficient): dt.NUMERIC

    OUTPUT
        q: dt.NUMERIC
    """

    psr = pow(p / p_res, 2)

    result = pow(1 - psr, n)
    return result


def pressure_ratio_from_fetkovich_equation(
    q: dt.NUMERIC, q_max: dt.NUMERIC, n: dt.NUMERIC
) -> dt.NUMERIC:
    """
    Calculation of pressure ratio
    Based on re-arrange of Vogel equation

    INPUT:
        p_res (reservoir pressure): dt.NUMERIC
        q (flow rate): dt.NUMERIC
        q_max (max flow rate): dt.NUMERIC

    OUTPUT: dt.NUMERIC
    """
    qr = q / q_max

    pr = sqrt(1 - sqrt(qr, n), 2)

    return pr


def wiggin_equation(
        phase: dt.STRING, p: dt.NUMERIC, p_res: dt.NUMERIC
) -> dt.NUMERIC:
    """
    Calculation of flow rate ratio
    using Wiggin equation according to phase selection

    INPUT
        phase: str
        p (wellbore pressure): dt.NUMERIC
        p_res (reservoir pressure): dt.NUMERIC

    OUTPUT
        qr: dt.NUMERIC
    """

    # Initiate pressure ratio
    pr = p / p_res

    # calculation of flow rate ratio
    if (phase == "oil"):
        qr = 1 - (0.52 * pr) - (0.48 * pow(pr, 2))
    elif (phase == "water"):
        qr = 1 - (0.72 * pr) - (0.28 * pow(pr, 2))

    return qr


def pressure_ratio_from_wiggin_equation(phase: dt.STRING, q: dt.NUMERIC, q_max: dt.NUMERIC):
    """
    Calculation of pressure ratio (wellbore pressure)
    Based on re-arrange of Wiggin equation

    INPUT:
        p_res (reservoir pressure): dt.NUMERIC
        q (flow rate): dt.NUMERIC
        q_max (max flow rate): dt.NUMERIC

    OUTPUT: dt.NUMERIC
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
