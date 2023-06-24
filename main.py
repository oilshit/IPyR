import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, make_interp_spline

from ipr import ProductionPerformance

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1734
production1 = ProductionPerformance(reservoir_pressure)

# Initial testing in repr production instance
print(repr(production1))

separate_line()

# Add several data on the production instance
production_data = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

for data in production_data:
    production1.data.append(data)

print("Production data in production 1:")
print(production1.data)

separate_line()

# Another testing in repr production instance
print(repr(production1))

separate_line()

# Using Vogel Equation for calculating
## max flow rate using single data
for data in production1.data:
    print("q: %d, p: %d" % (data["q"], data["p"]))

    print("Max flow rate using Vogel equation: " + str(
        round(
            production1.calculate_q_max(
                "vogel",
                data
            )
        )
    ))

# Get production graph interval
## Based on max flow obtained from Vogel eq.

test_production_data_2 = production1.data[0]
q_max_2 = production1.calculate_q_max("vogel", test_production_data_2)
iteration_2 = 12

production_graph = production1.get_production_graph(
    q_max_2,
    iteration_2
)

flowrate_x_2 = [data["q"] for data in production_graph]
pressure_y_2 = [data["p"] for data in production_graph]

plt.plot(flowrate_x_2, pressure_y_2, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_2, pressure_y_2, label=("p_wf = " + str(production1.data[0]["p"])))

# =========================

test_production_data_3 = production1.data[1]
q_max_3 = production1.calculate_q_max("vogel", test_production_data_3)
iteration_3 = 12

production_graph = production1.get_production_graph(
    q_max_3,
    iteration_3
)

flowrate_x_3 = [data["q"] for data in production_graph]
pressure_y_3 = [data["p"] for data in production_graph]

plt.plot(flowrate_x_3, pressure_y_3, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_3, pressure_y_3, label=("p_wf = " + str(production1.data[1]["p"])))

# =========================

test_production_data_1 = production1.data[2]
q_max_1 = production1.calculate_q_max("vogel", test_production_data_1)
iteration_1 = 12

production_graph = production1.get_production_graph(
    q_max_1,
    iteration_1
)

flowrate_x = [data["q"] for data in production_graph]
pressure_y = [data["p"] for data in production_graph]

plt.plot(flowrate_x, pressure_y, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x, pressure_y, label=("p_wf = " + str(production1.data[2]["p"])))

# =========================

plt.xlim(0, q_max_3 + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.title("Several IPRs for several wellbore pressures")
plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()