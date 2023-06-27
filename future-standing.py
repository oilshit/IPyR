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

# Initial testing in repr production instance
print(repr(production_data))

separate_line()

# Add several data on the production instance
production_cases = [
    { "q": 1361, "p": 680.5 },
]

for data in production_cases:
    production_data.data.append(data)

print("Here is the production data:")
print(production_data.data)

separate_line()

# Another testing in repr production instance
print(repr(production_data))

separate_line()

# Using Standing Equation for calculating
## max flow rate using single data
for data in production_data.data:
    print("q: %d, p: %d" % (data["q"], data["p"]))

    j_present = round(production_data.calculate_present_pi(data), 2)
    q_max = round(production_data.calculate_q_max(reservoir_pressure, data), 2)
    j_future = round(production_data.calculate_future_pi(data), 2)
    future_q = round(production_data.calculate_future_q(data), 2)
    # future_q_max = round(production_data.calculate_q_max({
    #     "q": future_q,
    #     "p": 
    # }), 2)

    print("Reservoir pressure at present condition: " + str(reservoir_pressure))
    print("Pressure at present condition: " + str(production_data.data[0]["p"]))
    print("Flow rate at present condition: " + str(production_data.data[0]["q"]))
    print("Current Production Index (PI) (j_p): " + str(j_present))
    print("Max flow rate using Standing equation (present) (stbd): " + str(q_max))

    separate_line()
    
    print("Future Production Index (PI) (j_f): " + str(j_future))
    print("Reservoir pressure at future condition: " + str(production_data.future_p_res))
    print("Flow rate at future condition: " + str(future_q))

#     plt.scatter(production_data.data[0]["q"], production_data.data[0]["p"], label="a")
#     plt.scatter(q_max, 0, label="b")
#     plt.scatter(future_q, 680.5 * 0.8, label="c")

# plt.legend()
# plt.show()