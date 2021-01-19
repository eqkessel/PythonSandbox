# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:34:13 2019

@author: redne
"""

def calc_fuel(mass):
    return int(mass / 3) - 2

data = input("Enter data:\n")

masses = data.split("\n")
print(masses)

fuel = 0
for part in masses:
    fuel += calc_fuel(int(part))
    
print("fuel needed is ", fuel)