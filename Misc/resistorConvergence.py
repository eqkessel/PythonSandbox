RESISTANCE = 10

# 2 Initial series resistors
network_resistance = 2 * RESISTANCE
num_resistors = 2

while True:
    last_network_resistance = network_resistance
    network_resistance = (last_network_resistance * RESISTANCE) /\
        (last_network_resistance + RESISTANCE) # Parallel resistor
    network_resistance += RESISTANCE # Series resistor

    # Within 1%?
    if abs(last_network_resistance - network_resistance) /\
        last_network_resistance < 0.01:
        break
    # Else,
    num_resistors += 2

print(f"Number of resistors required: {num_resistors}")
print(f"Final resistance of {num_resistors}-resistor network:\
    {last_network_resistance}")
print(f"Resistance if adding an additional stage: {network_resistance}")
