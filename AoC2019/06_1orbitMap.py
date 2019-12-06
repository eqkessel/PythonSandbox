# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:03:12 2019

@author: redne
"""

mapRaw = input("Enter map data:\n")

orbitals = mapRaw.split("\n")

phonebook = {}

for satelite in orbitals:
    objs = satelite.split(")")
    phonebook[objs[1]] = objs[0]

checksum = 0

for start in phonebook.keys():
    if (start == "COM"):
        continue
    body = start
    while True:
        body = phonebook[body]
        checksum += 1
        if (body == "COM"):
            break
        
print("\nOrbit Count Checksum:", checksum)
        