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

addressSanta = []
addressMe = []

body = "SAN"
while True:
    body = phonebook[body]
    addressSanta.append(body)
    if (body == "COM"):
        break
    
body = "YOU"
while True:
    body = phonebook[body]
    addressMe.append(body)
    if (body == "COM"):
        break
    
node = "COM"
for body in addressSanta:
    if (body in addressMe):
        node = body
        break
    
transfers = addressSanta.index(node) + addressMe.index(node)
print("\nNumber of transfers required:", transfers)