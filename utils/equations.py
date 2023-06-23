from data_types import *

def VogelEquation(p: NUMERIC, p_res: NUMERIC) -> NUMERIC:
    """
    Calculation of flow rate ratio
    Using Vogel Equation

    input:
        p (pressure): numeric
        p_res (reservoir presure): numeric

    output: numeric
    """
    pr = p / p_res          # pressure ratio

    return 1 - (0.2 * pr) - (0.8 * pr**2)