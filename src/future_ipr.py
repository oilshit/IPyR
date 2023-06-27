"""
future_ipr.py

Calculation of future production performance
"""

from src.utils import dt
from .utils import *

STANDARD_PRESSURE = 14.7                              # in psia
STANDARD_TEMPERATURE = 60                             # in Fahrenheit

class Production:
    """
    Production performance instance
    """

    def __init__(self, p_res: dt.NUMERIC):
        """
        Initiation of production performance instance

        INPUT
            p_res (Reservoir pressure) : numeric

            data (Flow rate, pressure) : { "q": numeric, "p": numeric }[]
                Default: []
        """

        self.data = []
        self.production_change = 0
        self.water_cut = 0
        self.future_water_cut = 0
        self.p_res = p_res
        self.future_p_res = self.p_res * (1 - self.production_change)

    def __repr__(self):
        data = "".join(["    " + dt.STRING(x) + ",\n" for x in self.data])

        class_repr = dt.STRING("Production performance data with reservoir pressure (psia) = "
                            + dt.STRING(self.p_res)
                            + "\nand "
                            + (
                                "some production data: [\n" + data + "]."
                                if len(self.data) > 0
                                else "empty production data."
                            )
                            )

        print(class_repr)

        return repr("Production instance exists!")
    
class OilWell(Production):
    """
    Production performance instance for oil wells
    """

    def __init__(self, p_res: dt.NUMERIC):
        super().__init__(p_res)

    def calculate_q_max(self, p_res: dt.NUMERIC, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Calculate max flow rate of oil production

        INPUT
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            q_max (Max flow rate): numeric
        """

        # init flow rate ratio
        qr = eq.vogel_equation(data["p"], p_res)

        # calculate max flow rate
        q_max = data["q"] / qr
        return q_max
    
    def calculate_pwf(self, p_res, q: dt.NUMERIC, q_max: dt.NUMERIC) -> dt.NUMERIC:
        """
        Calculation of wellbore pressure (p_wf)

        INPUT:
            p_res (reservoir pressure): numeric
            q (flow rate): numeric
            q_max (max flow rate): numeric

        OUTPUT:
            p_wf = numeric
        """

        pressure_ratio = eq.pressure_ratio_from_vogel_equation(q, q_max)
        p_wf = pressure_ratio * p_res

        return p_wf
        

    def get_production_index(self, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Get production index according to
        slope between pressure at reservoir and current condition
        with flow rate at reservoir pressure = 0,
        the difference of flow rate is equal to the flow rate itself

        INPUT
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            j (Production Index (PI)): numeric
        """

        j = 1.8 * self.calculate_q_max(self.p_res, data) / self.p_res
        return j
    
    def calculate_present_pi(self, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Get present productivity index

        INPUT
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            j_p (Present Production Index (PI)): numeric
        """

        j = self.get_production_index(data)
        
        j_r = 1 / 1.8 * (1 + 0.8 * (data["p"] / self.p_res))
        j_p = j / j_r

        return j_p
    
    def calculate_future_p_res(self, production_change: dt.NUMERIC) -> dt.NUMERIC:
        """
        Get the future reservoir pressure
        If the production change exists

        INPUT
            production_change: numeric

        OUTPUT
            p_res_f (Future reservoir presssure): numeric
        """

        self.production_change = production_change

        p_res_f = self.p_res * (1 - production_change)
        return p_res_f
    
    def calculate_future_pi(self, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Calculate future production index

        INPUT
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            j_f (Future Production Index (PI)): numeric
        """

        # init squared pressure ratio
        p_res_f = self.future_p_res
        squared_pr = (p_res_f / self.p_res) ** 2
        
        # calculate future production index
        j_p = self.calculate_present_pi(data)
        j_f = j_p * squared_pr

        return j_f
    
    def calculate_future_q(self, data):
        j_f = self.calculate_future_pi(data)  # future production index
        p_res_f = self.future_p_res
        vogel_calculation = eq.vogel_equation(data["p"], p_res_f)

        q = (j_f * p_res_f / 1.8) * vogel_calculation

        return q
    
    def get_production_graph(self, q_max: dt.NUMERIC, n: dt.INT, p_res: dt.NUMERIC, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA):
        """
        Create plot of production data interval
        based on q_max estimation and n intervals

        INPUT:
            q_max: numeric
            n: int
            p_res (reservoir pressure): numeric
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT: { "q": numeric, "p": numeric }[]
        """

        pressure_list = [x["p"] for x in self.data] + [p_res]
        production_list = []

        if (n > 0):
            # Add data for each interval
            interval = p_res // n

            # Add pressure segments
            pressure_segment = STANDARD_PRESSURE
            while (pressure_segment < p_res):
                pressure_list.append(pressure_segment)
                pressure_segment += interval

            pressure_list.sort()

            # Add pressure list
            for p in pressure_list:
                production_list.append({
                    "q": round(q_max * eq.vogel_equation(p, p_res), 2),
                    "p": p,
                })

                print("q", )

            return production_list