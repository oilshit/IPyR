from src.future_ipr import OilWell

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

# Initial testing in repr production instance
print(repr(production_data))

separate_line()

# Add several data on the production instance
production_cases = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
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
    separate_line()
    separate_line()

    print("q: %d, p: %d" % (data["q"], data["p"]))

    j_present = round(production_data.calculate_present_pi("standing", data), 2)
    q_max = round(production_data.calculate_q_max("standing", reservoir_pressure, data), 2)
    j_future = round(production_data.calculate_future_pi("standing", data), 2)
    future_q = round(production_data.calculate_future_q("standing", data), 2)
    future_q_max = round(production_data.calculate_q_max("standing", production_data.future_p_res, {
        "q": future_q,
        "p": data["p"]
    }), 2)

    print("Current Production Index (PI) (j_p): " + str(j_present))
    print("Reservoir pressure at present condition: " + str(reservoir_pressure))
    print("Pressure at present condition: " + str(data["p"]))
    print("Flow rate at present condition: " + str(data["q"]))
    print("Max flow rate using Standing equation (present) (stbd): " + str(q_max))

    separate_line()
    
    print("Future Production Index (PI) (j_f): " + str(j_future))
    print("Reservoir pressure at future condition: " + str(production_data.future_p_res))
    print("Flow rate at future condition: " + str(future_q))
    print("Max flow rate using Standing equation (future) (stbd): " + str(future_q_max))

#     plt.scatter(production_data.data[0]["q"], production_data.data[0]["p"], label="a")
#     plt.scatter(q_max, 0, label="b")
#     plt.scatter(future_q, 680.5 * 0.8, label="c")

# plt.legend()
# plt.show()