# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:54:13 2020

@author: redne
"""

import numpy as np
import matplotlib.pyplot as plt

# Uses a lambda to create a function that behaves like an op-amp
def makeOpAmpFunc(gain, vcc, vdd = 0):
    if vcc <= vdd:
        raise ValueError("Vcc must have a higher potential than Vdd")
    return lambda ninv, inv : (np.clip((gain * (ninv - inv) + (vcc + vdd) / 2), vdd, vcc))

vcc = 9 # volts

v_out = makeOpAmpFunc(10, vcc)  # op-amp with gain of 1 connected with 9v and GND

ninv_inputs = np.linspace(0, vcc) # input voltages to non-inverting input
outputs = np.zeros_like(ninv_inputs)

for index in range(len(ninv_inputs)):
    outputs[index] = v_out(ninv_inputs[index], vcc / 2)
    
plt.plot(ninv_inputs, outputs)
