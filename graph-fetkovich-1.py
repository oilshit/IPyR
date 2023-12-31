import numpy as np
import matplotlib.pyplot as plt

from src.ipr import TwoPhaseProduction

# Let's test on creating our first performance
reservoir_pressure = 1734
production1 = TwoPhaseProduction(reservoir_pressure)

# Add several data on the production instance
production_data = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

for data in production_data:
    production1.data.append(data)

# Get production graph interval
## Based on max flow obtained from Fetkovich eq.
test_production_data_0 = production1.data[0]
q_max_0 = production1.calculate_q_max("fetkovich", test_production_data_0)
iteration_0 = 12

production_graph = production1.get_production_graph(
    "fetkovich",
    q_max_0,
    iteration_0
)

flowrate_x_0 = [data["q"] for data in production_graph]
pressure_y_0 = [data["p"] for data in production_graph]

plt.plot(flowrate_x_0, pressure_y_0, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_0, pressure_y_0, label=("p_wf = " + str(production1.data[0]["p"])))

# =========================

test_production_data_1 = production1.data[1]
q_max_1 = production1.calculate_q_max("fetkovich", test_production_data_1)
iteration_1 = 12

production_graph = production1.get_production_graph(
    "fetkovich",
    q_max_1,
    iteration_1
)

flowrate_x_1 = [data["q"] for data in production_graph]
pressure_y_1 = [data["p"] for data in production_graph]

plt.plot(flowrate_x_1, pressure_y_1, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_1, pressure_y_1, label=("p_wf = " + str(production1.data[1]["p"])))

# =========================

test_production_data_2 = production1.data[2]
q_max_2 = production1.calculate_q_max("fetkovich", test_production_data_2)
iteration_2 = 12

production_graph = production1.get_production_graph(
    "fetkovich",
    q_max_2,
    iteration_2
)

flowrate_x_2 = [data["q"] for data in production_graph]
pressure_y_2 = [data["p"] for data in production_graph]

plt.plot(flowrate_x_2, pressure_y_2, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_2, pressure_y_2, label=("p_wf = " + str(production1.data[2]["p"])))

# =========================

plt.xlim(0, q_max_1 + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.title("Several IPRs for several wellbore pressures\nUsing Fetkovich equation")
plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()