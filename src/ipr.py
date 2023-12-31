from .utils import *

STANDARD_PRESSURE = 14.7                              # in psia
STANDARD_TEMPERATURE = 60                             # in Fahrenheit

class Production:
    """
    Calculation of production performance of multi-phase of IPR
    """
    

    def __init__(self, p_res: dt.NUMERIC):
        """
        Calculation of production performance of multi-phase of IPR

        INPUT:
            p_res (Reservoir pressure) : numeric

            data (Flow rate, pressure) : { "q": numeric, "p": numeric }[]
                Default: []
        """

        self.p_res = p_res
        self.data = []

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


class TwoPhaseProduction(Production):
    def __init__(self, p_res: dt.NUMERIC):
        super().__init__(p_res)

    def calculate_q_max(
        self,
        method: dt.STRING,
        data: dt.FLOWRATE_PRESSURE_SINGLE_DATA
    ) -> dt.NUMERIC:
        """
        Calculation of max flow rate (q_max)

        INPUT:
            method: str
            data (Flow rate, pressure) : [{ "q": numeric, "p": numeric }]

        OUTPUT:
            q_max = numeric
        """

        try:
            if (not isinstance(method, dt.STRING)):
                raise TypeError

            if (method == "vogel"):
                # applied all parameters in Vogel equation
                q_max = data["q"] / eq.vogel_equation(
                    data["p"], self.p_res
                )

                return q_max

            elif (method == "fetkovich"):
                # Resolving n using power regression method
                production_x = [x["q"] for x in self.data]
                production_y = [
                    (self.p_res**2 - x["p"]**2) for x in self.data
                ]

                (C, n) = numerical.power_regression(production_x, production_y)

                # applied all parameters in Fetkovich Equation
                q_max = data["q"] / eq.fetkovich_equation(
                    p=data["p"],
                    p_res=self.p_res,
                    C=None,
                    n=n
                )

                return q_max

            else:
                raise err.MethodNotExistExecption

        except err.MethodNotExistExecption:
            print("Method of calculation does not exist.")
            return None

        except TypeError:
            print("Expected str value  for method, %s given" % (type(method)))
            return None

    def calculate_pwf(self, method: dt.STRING, q: dt.NUMERIC, q_max: dt.NUMERIC) -> dt.NUMERIC:
        """
        Calculation of wellbore pressure (p_wf)

        INPUT:
            q (flow rate): numeric
            q_max (max flow rate): numeric

        INPUT:
            p_wf = numeric
        """

        if (method == "vogel"):
            pressure_ratio = eq.pressure_ratio_from_vogel_equation(q, q_max)
        elif (method == "fetkovich"):
            # Resolving n using power regression method
            production_x = [x["q"] for x in self.data]
            production_y = [
                (self.p_res**2 - x["p"]**2) for x in self.data
            ]

            (C, n) = numerical.power_regression(production_x, production_y)

            pressure_ratio = eq.pressure_ratio_from_fetkovich_equation(q, q_max, n)

        p_wf = pressure_ratio * self.p_res

        return p_wf

    def get_production_graph(self, method: dt.STRING, q_max: dt.NUMERIC, n: dt.INT):
        """
        Create plot of production data interval
        based on q_max estimation and n intervals

        INPUT:
            q_max: numeric
            n: int

        OUTPUT: { "q": numeric, "p": numeric }[]
        """

        pressure_list = [x["p"] for x in self.data] + [self.p_res]
        production_list = []

        if (n > 0):
            # Add data for each interval
            interval = self.p_res // n

            # Add pressure segments
            pressure_segment = STANDARD_PRESSURE
            while (pressure_segment < self.p_res):
                pressure_list.append(pressure_segment)
                pressure_segment += interval

            pressure_list.sort()

            # Add pressure list
            for p in pressure_list:
                if (method == "vogel"):
                    production_list.append({
                        "p": p,
                        "q": round(q_max * eq.vogel_equation(p, self.p_res), 2),
                    })
                elif (method == "fetkovich"):
                    production_x = [x["q"] for x in self.data]
                    production_y = [
                        (self.p_res**2 - x["p"]**2) for x in self.data
                    ]

                    (C, n) = numerical.power_regression(production_x, production_y)

                    production_list.append({
                        "p": p,
                        "q": round(q_max * eq.fetkovich_equation(p, self.p_res, None, n), 2),
                    })

            return production_list


class ThreePhaseProduction(Production):
    """
    Three-phase of reservoir production performance
    """

    def __init__(self, p_res: dt.NUMERIC, water_cut: dt.NUMERIC):
        super().__init__(p_res)

        self.water_cut = water_cut

    def calculate_q_max(self, phase: dt.STRING, method: dt.STRING, data: dt.FLOWRATE_PRESSURE_SINGLE_DATA) -> dt.NUMERIC:
        """
        Calculate max flow rate (q_max)
        According to phase and method selection

        input
            phase: str
            method: str
            data (Flow rate, pressure) : [{ "q": numeric, "p": numeric }]

        OUTPUT:
            q_max = numeric
        """

        try:
            if (phase not in dt.PHASE_DATA):
                raise err.PhaseNotExistsException

            if (not isinstance(method, dt.STRING)):
                raise TypeError

            if (method == "wiggin"):
                q_ratio = eq.wiggin_equation(phase, data["p"], self.p_res)

                if (phase == "oil"):
                    q = data["q"]
                elif (phase == "water"):
                    q = data["q"] / ((1 / self.water_cut) - 1)

                q_max = q / q_ratio

                return q_max

        except err.PhaseNotExistsException:
            print(
                "Phase selected doesn't exist.\n" +
                "Available phase: 'oil' and 'water'"
            )
            return None

        except TypeError:
            print("Expected str value  for method, %s given" % (type(method)))
            return None

    def calculate_pwf(self, phase: dt.STRING, q: dt.NUMERIC, q_max: dt.NUMERIC):
        """
        Calculation of wellbore pressure (p_wf)
        Using Vogel equations only

        INPUT:
            q (flow rate): numeric
            q_max (max flow rate): numeric

        INPUT:
            p_wf = numeric
        """

        pressure_ratio = eq.pressure_ratio_from_wiggin_equation(phase, q, q_max)
        p_wf = pressure_ratio * self.p_res

        return p_wf

    def get_production_graph(self, phase: dt.STRING, q_max: dt.NUMERIC, n: dt.INT):
        """
        Create plot of production data interval
        based on q_max estimation and n intervals

        INPUT:
            phase: str
            q_max: numeric
            n: int

        OUTPUT: { "q": numeric, "p": numeric }[]
        """

        pressure_list = [self.p_res]
        production_list = []

        if (n > 0):
            # Add data for each interval
            interval = self.p_res // n

            # Add pressure segments
            pressure_segment = STANDARD_PRESSURE
            while (pressure_segment < self.p_res):
                pressure_list.append(pressure_segment)
                pressure_segment += interval

            pressure_list.sort()

            # Add pressure list
            for p in pressure_list:
                production_list.append({
                    "p": p,
                    "q": round(q_max * eq.wiggin_equation(phase, p, self.p_res), 2),
                })

            return production_list
