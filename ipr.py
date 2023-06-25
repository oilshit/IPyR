from utils.errors import *
from utils.data_types import *

from utils.equations import *

from utils.numericals import *

STANDARD_PRESSURE = 14.7                              # in psia

class ProductionPerformance:
    """
    Calculation of production performance of multi-phase of IPR
    """

    def __init__(self, p_res: NUMERIC):
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
        data = "".join(["    " + STRING(x) + ",\n" for x in self.data])

        class_repr = STRING("Production performance data with reservoir pressure (psia) = "
                            + STRING(self.p_res)
                            + "\nand "
                            + (
                                "some production data: [\n" + data + "]."
                                if len(self.data) > 0
                                else "empty production data."
                            )
                            )

        print(class_repr)

        return repr("Production instance exists!")
    
class TwoPhaseProduction(ProductionPerformance):
    def calculate_q_max(
        self,
        method: STRING,
        data: FLOWRATE_PRESSURE_SINGLE_DATA
    ) -> NUMERIC:
        """
        Calculation of max flow rate (q_max)

        INPUT:
            method: str
            data (Flow rate, pressure) : [{ "q": numeric, "p": numeric }]

        INPUT:
            q_max = numeric
        """

        try:
            if (not isinstance(method, STRING)):
                raise TypeError

            elif (method == "vogel"):
                # applied all parameters in Vogel equation
                q_max = data["q"] / VogelEquation(
                    data["p"], self.p_res
                )

                return q_max
            
            elif (method == "fetkovich"):
                # Resolving n using power regression method
                production_x = [x["q"] for x in self.data]
                production_y = [
                    (self.p_res**2 - x["p"]**2) for x in self.data
                ]

                (C, n) = PowerRegression(production_x, production_y)

                # applied all parameters in Fetkovich Equation
                q_max = data["q"] / FetkovichEquation(
                    p=data["p"],
                    p_res=self.p_res,
                    C=None,
                    n=n
                )

                return q_max

            else:
                raise MethodNotExistExecption

        except MethodNotExistExecption:
            print("Method of calculation does not exist.")

        except TypeError:
            print("Expected str value, %s given" % (type(method)))

    def calculate_pwf(self, q: NUMERIC, q_max: NUMERIC):
        """
        Calculation of wellbore pressure (p_wf)
        Using Vogel equations only

        INPUT:
            q (flow rate): numeric
            q_max (max flow rate): numeric

        INPUT:
            p_wf = numeric
        """

        pressure_ratio = PressureRatioFromVogelEquation(q, q_max)
        p_wf = pressure_ratio * self.p_res

        return p_wf

    def get_production_graph(self, q_max: NUMERIC, n: INT):
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
                production_list.append({ 
                    "p": p,
                    "q": round(q_max * VogelEquation(p, self.p_res), 2),
                });
    
            return production_list

# class ThreePhaseProduction(ProductionPerformance):
    