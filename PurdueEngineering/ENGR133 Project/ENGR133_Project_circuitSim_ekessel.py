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

import os
import sys
import json
from types import SimpleNamespace # Container where values can be accessed like members
from collections import namedtuple

from ENGR133_Project_circuitSim_funcs_ekessel import * # Import everything

''' ===== Data/File Loading Section ===== '''

filedir = os.path.dirname(os.path.abspath(__file__)) # Locate this file and save directory
DEFAULTS_FNAME = "ENGR133_Project_circuitSim_defaults_ekessel.json"

# Ask the use whether they want to load default data, load a different file, or input data manually
options = ["Load default values.", "Load from file.", "Enter manually or calculate."]
print("\nPlease select a mode or 0 to exit:")
for idx, option in enumerate(options):
    print(f" {idx + 1}) {option}")

while True: # Loop until valid input is given
    instr = input("Enter a mode -> ")
    try:
        inval = int(instr)
        if not (0 <= inval <= len(options)):
            raise ValueError(f"Invalid entry: Please enter a number 0-{len(options)}")
        break
    except ValueError as e:
        print(f"Error: {e}")

if inval == 0: # Exit
    print("Exiting...")
    sys.exit()
elif inval == 3: # Manual input
    raise NotImplementedError("Coming soon!")
    c = None # Dummy, replace with input function
else:
    if inval == 1: # Default file
        json_path = os.path.join(filedir, DEFAULTS_FNAME)
        
    else: # User input for filename
        while True: # Loop until valid input is given
            instr = input("Enter the name/path to a .json constants file (or 'exit' to exit) -> ")
            try:
                if instr == 'exit':
                    print("Exiting...")
                    sys.exit()
                    
                path = os.path.abspath(instr)
                if not os.path.isfile(path):
                    raise ValueError("The path you specified does not lead to a file")
                if not path.lower().endswith(('.json')):
                    raise ValueError("The file you specified is not a .json file")
                    
                validateJSONconstants(path)   # UDF to check file has everything needed
                
                json_path = path
                break
            
            except ValueError as e:
                print(f"Error: {e}")
                
    # We have a valid path now, load the constants
    with open(json_path) as json_file_obj:
        c = json.load(json_file_obj, object_hook = lambda d : SimpleNamespace(**d))
        c.A = dBtoAmp(c.GAIN)
        
print("\nThe simulation constants are:")
for value_name in CONST_NAMES:
    print(f" {value_name:4} = {c.__getattribute__(value_name):7} [{CONST_NAMES[value_name]}]")
  
      
''' ===== Simulation Section ===== '''

# Differential equation. Recieves t and a state vector Q and returns dQ/dt
def dQ_dt(t, Q, consts, Vout):
    return [((Vout - consts.VREF) /  consts.R1) - (Q[0] / (consts.R1 * consts.C))]

op_amp = makeOpAmpFunc(c.A, c.VCC, c.VDD)  # Make the op-amp function

# Arrays to hold simulation data
time_steps_s = np.arange(c.T_0, c.T_F, c.T_S)   # Time steps for the simulation
cap_charge_C = np.zeros_like(time_steps_s)  # Charge on the capacitor (Coulombs)
output_volts = np.zeros_like(time_steps_s)  # Output voltage of the op-amp
invert_inp_V = np.zeros_like(time_steps_s)  # Inverting input voltage on the op-amp
ninvrt_inp_V = np.zeros_like(time_steps_s)  # Non-inverting input voltage on the op-amp

# Initialize the numerical integrator
rk4 = ode(dQ_dt).set_integrator('dopri5')   # Runge-Kutta method of order (4)5
rk4.set_initial_value([cap_charge_C[0]], c.T_0) # Specify the IVP conditions

# Run the simulation
ts_index = 1 # Current time-step index
while (rk4.successful() and rk4.t < c.T_F and ts_index < len(time_steps_s)):
    # Multiple checks to verify validity of integration process
    
    # Calculate voltages on op-amp inputs (using last voltage) and op-amp output
    invert_inp_V[ts_index] = c.VREF + (cap_charge_C[ts_index - 1] / c.C)
    ninvrt_inp_V[ts_index] = c.VREF + ((output_volts[ts_index - 1] - c.VREF) * c.R2 / (c.R2 + c.R3))
    output_volts[ts_index] = op_amp(ninvrt_inp_V[ts_index], invert_inp_V[ts_index])
    
    rk4.set_f_params(c, output_volts[ts_index]) # Set parameters for the differential eq.
    rk4.integrate(time_steps_s[ts_index]) # Run the numerical integration
    cap_charge_C[ts_index] = rk4.y[0]   # Extract capacitor charge from the integrator
    
    ts_index += 1   # Move on to the next time step


''' ===== Plot/Output Section ===== '''

fig = plt.figure()

ax1 = fig.add_axes((0.1, 0.22, 0.8, 0.7))

ax1.set_xlabel('Time, seconds')
ax1.set_ylabel('Volts', color='tab:blue')
ax1.plot(time_steps_s, output_volts, '-', label='Output [V]', color='tab:purple')
ax1.plot(time_steps_s, ninvrt_inp_V, '--', label='Non-inverting input [V]', color='tab:green')
ax1.plot(time_steps_s, invert_inp_V, '--', label='Inverting input [V]', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx() # Create graph with twinned x-axis

ax2.set_ylabel('Capacitor Charge, Coulombs', color='tab:orange')
ax2.plot(time_steps_s, cap_charge_C, ':', label='Capacitor Charge [C]', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

plt.title("Simulation Data vs. Time")

fig.legend(ncol=3, loc="upper right", bbox_to_anchor=(0., 0.02, 1., 0.1), mode="expand")

fig.tight_layout()
plt.show()

# ninv_inputs = np.linspace(c.VDD, c.VCC) # input voltages to non-inverting input
# outputs = np.zeros_like(ninv_inputs)

# for index in range(len(ninv_inputs)):
#     outputs[index] = op_amp(ninv_inputs[index], c.VCC / 2)
    
# plt.plot(ninv_inputs, outputs)
