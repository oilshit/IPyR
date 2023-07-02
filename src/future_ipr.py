"""
future_ipr.py

Calculation of future production performance
"""

import matplotlib.pyplot as plt
import math

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
                DEFAULT: []

            future_data (Flow rate, pressure) : { "q": numeric, "p": numeric }[]
                DEFAULT: []

            water_cut: numeric
                DEFAULT: 0

            future_water_cut: numeric
                DEFAULT: 0

            production_change: numeric
                DEFAULT: 0

            future_p_res (Future reservoir pressure): numeric
        """

        self.production_change = 0
        self.water_cut = 0
        self.future_water_cut = 0
        
        self.data = []
        self.future_data = []

        self.p_res = p_res
        self.future_p_res = self.p_res * (1 - self.production_change)

    def insert_data(self, data: dt.FLOWRATE_PRESSURE_DATA) -> None:
        for i in data:
            self.data.append(i)

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

    def insert_future_data(self, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_DATA) -> None:
        for i in data:
            print(i)
            if (method == "standing" or method == "eckmeir"):
                self.future_data.append({ "q": self.calculate_future_q("eckmeir" if method == "eckmeir" else method, i), "p": i["p"] })

    def calculate_q_max(
            self,
            method: dt.STRING,
            p_res: dt.NUMERIC,
            data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Calculate max flow rate of oil production

        INPUT
            method: str
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            q_max (Max flow rate): numeric
        """

        if (
            method == "standing"
            or method == "eckmeir_present"
        ):
            # applied all parameters in Standing equation
            q_max = data["q"] / eq.vogel_equation(
                data["p"], p_res
            )

            return q_max

        elif (method == "fetkovich"):
            # Resolving n using power regression method
            production_x = [x["q"] for x in self.data]
            production_y = [(self.p_res**2 - x["p"]**2) for x in self.data]

            if (len(self.data) == 1):
                production_x.append(1.00000001)
                production_y.append(1.00000001)

            (C, n) = numerical.power_regression(production_x, production_y)

            print("n =", n, "c =", C)

            # applied all parameters in Fetkovich Equation
            q_max = self.calculate_future_pi(method, data) * math.pow(p_res**2 - data["p"]**2, n)
            print(q_max)

            return q_max
        
        elif (method == "eckmeir_future"):
            # future flow max using Eckmeir equation
            pr = math.pow(self.future_p_res / self.p_res, 3)
            present_q_max = self.calculate_q_max("eckmeir_present", self.p_res, self.data[-1])

            # print(present_q_max)

            return pr * present_q_max
    
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
        

    def get_production_index(self, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
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

        j = 1.8 * self.calculate_q_max(method, self.p_res, data) / self.p_res
        return j
    
    def calculate_present_pi(self, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Get present productivity index

        INPUT
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            j_p (Present Production Index (PI)): numeric
        """

        if (method == "standing" or method == "eckmeir"):
            j = self.get_production_index("standing", data)
            
            j_r = 1 / 1.8 * (1 + 0.8 * (data["p"] / self.p_res))
            j_p = j / j_r

            return j_p
    
        elif (method == "fetkovich"):
            production_x = [x["q"] for x in self.data]
            production_y = [(self.p_res**2 - x["p"]**2) for x in self.data]

            if (len(self.data) == 1):
                production_x.append(0.1)
                production_y.append(0.1)
            
            (C, n) = numerical.power_regression(production_x, production_y)

            print("ini n =", n, C)

            if (len(self.data) >= 1):
            #     return C    
            # else:
                psr = math.pow(self.p_res**2 - data["p"]**2, n)
                return data["q"] / psr
    
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
    
    def calculate_future_pi(self, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Calculate future production index

        INPUT
            method: string
            data: (Flow rate, pressure) : { "q": numeric, "p": numeric }

        OUTPUT
            j_f (Future Production Index (PI)): numeric
        """

        if (method == "standing" or method == "eckmeir"):
            # init squared pressure ratio
            p_res_f = self.future_p_res
            squared_pr = (p_res_f / self.p_res) ** 2
            
            # calculate future production index
            j_p = self.calculate_present_pi(method, data)
            j_f = j_p * squared_pr

            return j_f
        
        elif (method == "fetkovich"):
            future_p_res = self.calculate_future_p_res(self.production_change)
            j_p = self.calculate_present_pi(method, data)
            j_f = j_p * (future_p_res / self.p_res)

            return j_f
    
    def calculate_future_q(self, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA):
        if (method == "standing"):
            j_f = self.calculate_future_pi(method, data)  # future production index
            p_res_f = self.future_p_res
            vogel_calculation = eq.vogel_equation(data["p"], p_res_f)

            q = (j_f * p_res_f / 1.8) * vogel_calculation

            return q
        
        elif (method == "fetkovich"):
            production_x = [x["q"] for x in self.data]
            production_y = [(self.p_res**2 - x["p"]**2) for x in self.data]

            if (len(self.data) == 1):
                production_x.append(1.00000001)
                production_y.append(1.00000001)

            (C, n) = numerical.power_regression(production_x, production_y)

            future_p_res = self.calculate_future_p_res(self.production_change)

            psr = math.pow(future_p_res**2 - data["p"]**2, n)
            j_f = self.calculate_future_pi(method, data)
            q = j_f * psr

            return q
        
        elif (method == "eckmeir"):
            print(self.future_p_res, self.p_res)
            pr = math.pow(self.future_p_res / self.p_res, 3)
            print(pr)

            q = pr * data["q"]
            print(q)
            return q
    
    def get_production_graph(self, method: dt.STRING, q_max: dt.NUMERIC, n: dt.INT, p_res: dt.NUMERIC, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA):
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
                if (method == "standing" or method == "eckmeir"):
                    production_list.append({
                        "q": round(q_max * eq.vogel_equation(p, p_res), 2),
                        "p": p,
                    })

                elif (method == "fetkovich"):
                    production_x = [x["q"] for x in self.data]
                    production_y = [(p_res**2 - x["p"]**2) for x in self.data]

                    if (len(self.data) == 1):
                        production_x.append(1.00000001)
                        production_y.append(1.00000001)

                    (C, n) = numerical.power_regression(production_x, production_y)

                    production_list.append({
                        "p": p,
                        "q": round(q_max * eq.fetkovich_equation(p, p_res, None, n), 2),
                    })

            return production_list