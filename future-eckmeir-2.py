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

# Initial testing in repr production instance
print(repr(production_data))

separate_line()

# Add several data on the production instance
production_cases = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

production_data.insert_data(production_cases)

print("Here is the production data:")
print(production_data.data)

separate_line()

# Another testing in repr production instance
print(repr(production_data))

separate_line()

production_data.insert_future_data("eckmeir", production_data.data)
print(production_data.future_data)

# Using Eickmeir Equation for calculating
## max flow rate using single data
for data in production_data.data:
    print("q: %d, p: %d" % (data["q"], data["p"]))

    q_max = round(production_data.calculate_q_max("eckmeir_present", reservoir_pressure, data), 2)    
    future_q = round(production_data.calculate_future_q("eckmeir", data), 2)
    # print("Future q", future_q)
    future_q_max = production_data.calculate_q_max(
        "eckmeir_future",
        production_data.future_p_res, {
        "q": future_q,
        "p": production_data.data[-1]["p"]
    })

    # print("Future Q_max", future_q_max)

    print("Reservoir pressure at present condition: " + str(reservoir_pressure))
    print("Pressure at present condition: " + str(production_data.data[0]["p"]))
    print("Flow rate at present condition: " + str(production_data.data[0]["q"]))
    print("Max flow rate using Eickmeir equation (present) (stbd): " + str(q_max))

    separate_line()
    
    print("Reservoir pressure at future condition: " + str(production_data.future_p_res))
    print("Max flow rate using Eickmeir equation (future) (stbd): " + str(future_q_max))

    separate_line()
#     plt.scatter(production_data.data[0]["q"], production_data.data[0]["p"], label="a")
#     plt.scatter(q_max, 0, label="b")
#     plt.scatter(future_q, 680.5 * 0.8, label="c")

# plt.legend()
# plt.show()