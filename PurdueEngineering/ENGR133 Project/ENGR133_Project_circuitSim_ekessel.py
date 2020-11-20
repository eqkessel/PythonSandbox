# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:54:13 2020

@author: redne
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

def dBtoAmp(decibels): return (10 ** (decibels / 20))

# Use a namedtuple type to create a sinmple container with named member elements
Consts = namedtuple('Consts', ['C', 'R1', 'R2', 'R3', 'A', 'VCC', 'VDD'], defaults=[0])
c = Consts(C    = 10e-6, # Farads
           R1   = 10e+3, # Ohms
           R2   = 1e+3,  # Ohms
           R3   = 1e+3,  # Ohms
           A    = dBtoAmp(100), # Given in decibels, convert to unitless amplification
           VCC  = 9,     # Volts, positive rail
           VDD  = 0)     # Volts, negative rail


# Uses a lambda to create a function that behaves like an op-amp
def makeOpAmpFunc(gain, vcc, vdd = 0):
    if vcc <= vdd:
        raise ValueError("Vcc must have a higher potential than Vdd")
    return lambda ninv, inv : (np.clip((gain * (ninv - inv) + (vcc + vdd) / 2), vdd, vcc))


v_out = makeOpAmpFunc(c.A, c.VCC, c.VDD)  # op-amp with gain of 1 connected with 9v and GND

ninv_inputs = np.linspace(c.VDD, c.VCC) # input voltages to non-inverting input
outputs = np.zeros_like(ninv_inputs)

for index in range(len(ninv_inputs)):
    outputs[index] = v_out(ninv_inputs[index], c.VCC / 2)
    
plt.plot(ninv_inputs, outputs)
