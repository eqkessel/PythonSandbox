#******************************************************************************
#
# ENGR 133 - FA 20 - LC4-02
# Personal Project - Ethan Kessel (ekessel@purdue.edu)
#
# ENGR133_Project_circuitSim_ekessel.py
#
# Models an astable multivibrator oscilator circuit built using an op-amp using
# the integrate module of scipy.
#
#==============================================================================
#
# MIT License
#
# Copyright (c) 2020 Ethan Kessel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#******************************************************************************

import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from collections import namedtuple

from ENGR133_Project_circuitSim_funcs_ekessel import * # Import everything

'''
Circuit Values in Actual Circuit:
    C:  Ceramic Capacitor 105 = 1 uF = 1e-6 F
    R1: 100kOhm = 100e+3 Ohm
    R2 = R3: 10kOhm = 10e+3 Ohm
    Op-Amp: LM358-N, gain 100 dB
    Vcc:  +9v
    Vdd:  0v
    Vref: +4.5v
'''

# Use a namedtuple type to create a sinmple container with named member elements
Consts = namedtuple('Consts', ['C', 'R1', 'R2', 'R3', 'A', 'VCC', 'VDD', 'VREF'])
c = Consts(C    = 1e-6,     # Farads
           R1   = 100e+3,   # Ohms
           R2   = 10e+3,    # Ohms
           R3   = 10e+3,    # Ohms
           A    = dBtoAmp(100), # Given in decibels, convert to unitless amplification
           VCC  = 9,        # Volts, positive power rail
           VDD  = 0,        # Volts, negative power rail
           VREF = 4.5)      # Volts, fixed reference voltage

# Differential equation. Recieves t and a state vector Q and returns dQ/dt
def dQ_dt(t, Q, consts, Vout):
    return [((Vout - consts.VREF) /  consts.R1) - (Q[0] / (consts.R1 * consts.C))]

op_amp = makeOpAmpFunc(c.A, c.VCC, c.VDD)  # op-amp function

t0_s = 0.0   # Simulation start time
tf_s = 1.    # Simulation stop time in seconds
dt_s = 0.001 # Simulation time step in seconds

# Arrays to hold simulation data
time_steps_s = np.arange(t0_s, tf_s, dt_s)  # Time steps for the simulation
cap_charge_C = np.zeros_like(time_steps_s)  # Charge on the capacitor (Coulombs)
output_volts = np.zeros_like(time_steps_s)  # Output voltage of the op-amp
invert_inp_V = np.zeros_like(time_steps_s)  # Inverting input voltage on the op-amp
ninvrt_inp_V = np.zeros_like(time_steps_s)  # Non-inverting input voltage on the op-amp

# Initialize the numerical integrator
rk4 = ode(dQ_dt).set_integrator('dopri5')   # Runge-Kutta method of order (4)5
rk4.set_initial_value([cap_charge_C[0]], t0_s)  # Specify the IVP conditions

ts_index = 1 # Current time-step index
while (rk4.successful() and rk4.t < tf_s and ts_index < len(time_steps_s)):
    # Multiple checks to verify validity of integration process
    
    # Calculate voltages on op-amp inputs (using last voltage) and op-amp output
    invert_inp_V[ts_index] = c.VREF + (cap_charge_C[ts_index - 1] / c.C)
    ninvrt_inp_V[ts_index] = c.VREF + ((output_volts[ts_index - 1] - c.VREF) * c.R2 / (c.R2 + c.R3))
    output_volts[ts_index] = op_amp(ninvrt_inp_V[ts_index], invert_inp_V[ts_index])
    
    rk4.set_f_params(c, output_volts[ts_index]) # Set parameters for the differential eq.
    rk4.integrate(time_steps_s[ts_index])
    cap_charge_C[ts_index] = rk4.y[0]   # Extract capacitor charge from the integrator
    
    ts_index += 1

''' Plot Results '''
fig, ax1 = plt.subplots()

ax1.set_xlabel('Time, seconds')
ax1.set_ylabel('Volts')
ax1.plot(time_steps_s, output_volts, label='Output')
ax1.plot(time_steps_s, ninvrt_inp_V, label='Non-inverting input')
ax1.plot(time_steps_s, invert_inp_V, label='Inverting input')

ax2 = ax1.twinx() # Create graph with twinned x-axis

ax2.set_ylabel('Charge, Coulombs')
ax2.plot(time_steps_s, cap_charge_C, label='Capacitor Charge', color='tab:red')

fig.legend()

fig.tight_layout()
plt.show()

# ninv_inputs = np.linspace(c.VDD, c.VCC) # input voltages to non-inverting input
# outputs = np.zeros_like(ninv_inputs)

# for index in range(len(ninv_inputs)):
#     outputs[index] = op_amp(ninv_inputs[index], c.VCC / 2)
    
# plt.plot(ninv_inputs, outputs)
