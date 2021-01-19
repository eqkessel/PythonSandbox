# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:34:13 2019

@author: redne
"""

def calc_fuel(mass):
    total_fuel = 0
    working_mass = mass
    while True:
        next_mass = int(working_mass / 3) - 2
        if (next_mass <= 0):
            return total_fuel
        total_fuel += next_mass
        working_mass = next_mass

print("Validating...\n")
if (calc_fuel(14) == 2):
    print("...14 ok\n")
if (calc_fuel(1969) == 966):
    print("...1969 ok\n")
if (calc_fuel(100756) == 50346):
    print("...100756 ok\n")

data = input("Enter data:\n")

masses = data.split("\n")
print(masses)

fuel = 0
for part in masses:
    fuel += calc_fuel(int(part))
    
print("fuel needed is ", fuel)