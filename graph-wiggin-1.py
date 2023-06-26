import numpy as np
import matplotlib.pyplot as plt

from src.ipr import ThreePhaseProduction

# Let's test on creating our first performance
reservoir_pressure = 1734
water_cut = 0.3
production1 = ThreePhaseProduction(reservoir_pressure, water_cut)

# Add several data on the production instance
production_data = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

for data in production_data:
    production1.data.append(data)

# Get production graph interval
## Based on max flow obtained from Wiggin eq.
test_production_data_0 = production1.data[2]
qo_max_0 = production1.calculate_q_max("oil", "wiggin", test_production_data_0)
qw_max_0 = production1.calculate_q_max("water", "wiggin", test_production_data_0)
iteration_0 = 12

water_data = production1.get_production_graph(
    "water",
    qw_max_0,
    iteration_0
)

oil_data = production1.get_production_graph(
    "oil",
    qo_max_0,
    iteration_0
)

flowrate_oilx_0 = [data["q"] for data in oil_data]
pressure_oily_0 = [data["p"] for data in oil_data]

plt.plot(flowrate_oilx_0, pressure_oily_0, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_oilx_0, pressure_oily_0, label="oil data")

flowrate_waterx_0 = [data["q"] for data in water_data]
pressure_watery_0 = [data["p"] for data in water_data]

plt.plot(flowrate_waterx_0, pressure_watery_0, linestyle="dashed", linewidth=.75)
plt.scatter(flowrate_waterx_0, pressure_watery_0, label="water data")

plt.scatter(
    [data["q"] for data in production_data],
    [data["p"] for data in production_data],
    label=("production data"))

# =========================


plt.xlim(0, qo_max_0 + 1000)
plt.ylim(0, reservoir_pressure + 1000)

plt.title("Several IPRs for several wellbore pressures\nUsing Wiggin equation")
plt.xlabel('Flow rate (stbd)')
plt.ylabel('Pressure (psia)')

plt.legend()

plt.show()