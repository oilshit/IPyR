import numpy as np
import matplotlib.pyplot as plt

from ipr import TwoPhaseProduction

# Let's test on creating our first performance
reservoir_pressure = 1734
production_data = TwoPhaseProduction(reservoir_pressure)

# Add several data on the production instance
production_case = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

for data in production_case:
    production_data.data.append(data)

# Get production graph interval
## Based on max flow obtained from Vogel eq.
test_production_data = production_data.data[2]
q_max_vogel = production_data.calculate_q_max("vogel", test_production_data)
iteration_0 = 12

vogel_graph = production_data.get_production_graph(
    "fetkovich",
    q_max_vogel,
    iteration_0
)

flowrate_x_0 = [data["q"] for data in vogel_graph]
pressure_y_0 = [data["p"] for data in vogel_graph]

plt.plot(flowrate_x_0, pressure_y_0, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_0, pressure_y_0, label="Vogel")

# Get production graph interval
## Based on max flow obtained from Fetkovich eq.
test_production_data = production_data.data[2]
q_max_fetkovich = production_data.calculate_q_max("fetkovich", test_production_data)
iteration_0 = 12

fetkovich_graph = production_data.get_production_graph(
    "fetkovich",
    q_max_fetkovich,
    iteration_0
)

flowrate_x_1 = [data["q"] for data in fetkovich_graph]
pressure_y_y = [data["p"] for data in fetkovich_graph]

plt.plot(flowrate_x_1, pressure_y_y, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_1, pressure_y_y, label="Fetkovich")

plt.scatter(
    [data["q"] for data in production_data.data], 
    [data["p"] for data in production_data.data], 
    label="Production data"
)

plt.xlim(0, q_max_vogel + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.title("Several IPRs for several methods\nTwo-phase production")
plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()