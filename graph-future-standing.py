from src.future_ipr import OilWell
from src.ipr import eq

import matplotlib.pyplot as plt

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1224.9
production_data = OilWell(reservoir_pressure)

production_data.water_cut = 0.3
production_data.future_water_cut = 0.3
production_data.production_change = 0.2

production_data.future_p_res = reservoir_pressure * (1 - production_data.production_change)

# Add several data on the production instance
production_cases = [
    { "q": 1361, "p": 680.5 },
]

for data in production_cases:
    production_data.data.append(data)

# Using Standing Equation for calculating
## max flow rate using single data
standing_data = production_data.data[0]

# Acquire several properties for production
j_present = round(production_data.calculate_present_pi(standing_data), 2)
q_max = round(production_data.calculate_q_max(reservoir_pressure, standing_data), 2)

j_future = round(production_data.calculate_future_pi(standing_data), 2)
future_p_res = production_data.future_p_res

future_q = round(production_data.calculate_future_q(standing_data), 2)
future_data = {
    "q": future_q,
    "p": 680.5
}
future_q_max = round(production_data.calculate_q_max(future_p_res, future_data), 2)

iter = 12

standing_graph = production_data.get_production_graph(q_max, iter, reservoir_pressure, standing_data)

flowrate_x = [data["q"] for data in standing_graph]
pressure_y = [data["p"] for data in standing_graph]

plt.plot(flowrate_x, pressure_y, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x, pressure_y, label="Standing (current)")

plt.scatter(
    [data["q"] for data in production_data.data], 
    [data["p"] for data in production_data.data], 
    label="Production data"
)

standing_future_graph = production_data.get_production_graph(future_q_max, iter, future_p_res, future_data)

flowrate_x_1 = [data["q"] for data in standing_future_graph]
pressure_y_1 = [data["p"] for data in standing_future_graph]

plt.plot(flowrate_x_1, pressure_y_1, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_x_1, pressure_y_1, label="Standing (3 years later)")

plt.scatter(future_data["q"], future_data["p"], label="Future")

plt.xlim(0, q_max + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()