from src.future_ipr import OilWell
from src.ipr import eq

import matplotlib.pyplot as plt

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1734
production_data = OilWell(reservoir_pressure)

production_data.water_cut = 0.3
production_data.future_water_cut = 0.3
production_data.production_change = 0.2

production_data.future_p_res = reservoir_pressure * (1 - production_data.production_change)

# Add several data on the production instance
production_cases = [
    { "q": 768, "p": 1335 },
]

for data in production_cases:
    production_data.data.append(data)

# Using Eckmeir Equation for calculating
## max flow rate using single data
eckmeir_data = production_data.data[-1]

# Acquire several properties for production
j_present = round(production_data.calculate_present_pi("eckmeir", eckmeir_data), 2)
q_max = round(production_data.calculate_q_max("eckmeir_present", reservoir_pressure, eckmeir_data), 2)

j_future = round(production_data.calculate_future_pi("eckmeir", eckmeir_data), 2)
future_p_res = production_data.future_p_res

future_q = round(production_data.calculate_future_q("eckmeir", eckmeir_data), 2)
future_data = {
    "q": future_q,
    "p": production_data.data[-1]["p"]
}
future_q_max = round(production_data.calculate_q_max("eckmeir_future", future_p_res, future_data), 2)

iter = 12

eckmeir_graph = production_data.get_production_graph("eckmeir", q_max, iter, reservoir_pressure, eckmeir_data)

flowrate_x = [data["q"] for data in eckmeir_graph]
pressure_y = [data["p"] for data in eckmeir_graph]

plt.plot(flowrate_x, pressure_y, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x, pressure_y, label="Eckmeir (current)")

plt.scatter(
    [data["q"] for data in production_data.data], 
    [data["p"] for data in production_data.data], 
    label="Production data"
)

eckmeir_future_graph = production_data.get_production_graph("eckmeir", future_q_max, iter, future_p_res, future_data)

flowrate_x_1 = [data["q"] for data in eckmeir_future_graph]
pressure_y_1 = [data["p"] for data in eckmeir_future_graph]

plt.plot(flowrate_x_1, pressure_y_1, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_1, pressure_y_1, label="Eckmeir (3 years later)")

plt.scatter(future_data["q"], future_data["p"], label="Future production data")

plt.xlim(0, q_max + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.title("Future Production Performance of Oil Well\nUsing Eckmeir Equation")
plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()