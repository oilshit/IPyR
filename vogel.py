from src.ipr import TwoPhaseProduction

def separate_line():
    print()

# Let's test on creating our first performance
reservoir_pressure = 1734
production_data = TwoPhaseProduction(reservoir_pressure)

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

# Using Vogel Equation for calculating
## max flow rate using single data
for data in production_data.data:
    print("q: %d, p: %d" % (data["q"], data["p"]))

    print("Max flow rate using Vogel equation: " + str(
        round(
            production_data.calculate_q_max(
                "vogel",
                data
            )
        )
    ))

