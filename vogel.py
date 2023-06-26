from src.ipr import TwoPhaseProduction

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1734
production1 = TwoPhaseProduction(reservoir_pressure)

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

