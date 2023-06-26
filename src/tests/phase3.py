from src.ipr import ThreePhaseProduction

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1734
water_cut = 0.3
production_data = ThreePhaseProduction(reservoir_pressure, water_cut)

# Initial testing in repr production instance
print(repr(production_data))

separate_line()

# Add several data on the production instance
data = [
    { "q": 252, "p": 1653 },
    { "q": 516, "p": 1507 },
    { "q": 768, "p": 1335 },
]

for data in data:
    production_data.data.append(data)

print("Here is the production data:")
print(production_data.data)

separate_line()

# Another testing in repr production instance
print(repr(production_data))

separate_line()

# Using Wiggin Equation for calculating
## max flow rate using single data for each phase
for data in production_data.data:
    print("q: %d, p: %d" % (data["q"], data["p"]))

    print("Max flow rate using Wiggin equation (oil phase): " + str(
        round(
            production_data.calculate_q_max(
                "oil",
                "wiggin",
                data
            )
        )
    ))

    print("Max flow rate using Wiggin equation (water phase): " + str(
        round(
            production_data.calculate_q_max(
                "water",
                "wiggin",
                data
            )
        )
    ))

