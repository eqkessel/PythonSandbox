# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 23:50:23 2019

@author: redne
"""

mass=input("input")
mass=mass.split("\n")
mass=[int(n) for n in mass]

def fuelCount(aMass):
    retval=int(aMass/3)-2
    if(retval<0):
        retval=0
    else:
        retval+=fuelCount(retval)
        
    return retval

fuel=0
for i in mass:
    fuel+=fuelCount(i)
    
print("Fuel is",fuel)