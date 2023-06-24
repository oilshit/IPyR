from .data_types import *

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
    result = 1 - (0.2 * pr) - (0.8 * pr**2)

    return result if result > 0 else 0.0001

def PressureRatioFromVogelEquation(q: NUMERIC, q_max: NUMERIC):
    """
    Calculation of p_wf (wellbore pressure)
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
    result = (-a - (b**2 - (4 * a * (c - qr)))**0.5) / (2 * a)

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

    psr = (p / p_res) ** 2

    result = (1 - psr) ** n
    return result

