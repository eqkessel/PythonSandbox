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
from tqdm import tqdm # Progress bar

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
elif inval == 3: # Manual input, load using UDF
    c = userInputCalculate(os.path.join(filedir, DEFAULTS_FNAME))
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
                    
                path = os.path.abspath(instr) # Locate absolute location of specified path
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
        # Load json but wrapping it into a SimpleNamespace
        c = json.load(json_file_obj, object_hook = lambda d : SimpleNamespace(**d))

c.A = dBtoAmp(c.GAIN)   # Compute the amplification constant from the gain in dB

# Display the constants for the simulation that were just loaded       
print("\nThe simulation constants are:")
for val_name in CONST_NAMES:
    print(f" {val_name:4} = {c.__getattribute__(val_name):7} [{CONST_NAMES[val_name]}]")


''' ===== Simulation Section ===== '''

# Differential equation function. Recieves t and a state vector Q and returns dQ/dt
def dQ_dt(t, Q, consts, Vout):
    return [((Vout - consts.VREF) /  consts.R1) - (Q[0] / (consts.R1 * consts.C))]

op_amp = makeOpAmpFunc(c.A, c.VCC, c.VEE)  # Make the op-amp function

# Arrays to hold simulation data
time_steps_s = np.arange(c.T_0, c.T_F, c.DT)    # Time steps for the simulation
cap_charge_C = np.zeros_like(time_steps_s)  # Charge on the capacitor (Coulombs)
output_volts = np.zeros_like(time_steps_s)  # Output voltage of the op-amp
invert_inp_V = np.zeros_like(time_steps_s)  # Inverting input voltage on the op-amp
ninvrt_inp_V = np.zeros_like(time_steps_s)  # Non-inverting input voltage on the op-amp

reference_V = np.full_like(time_steps_s, c.VREF) # Used in plotting later

# Initialize the numerical integrator
rk4 = ode(dQ_dt).set_integrator('dopri5')   # Runge-Kutta method of order (4)5
rk4.set_initial_value([cap_charge_C[0]], c.T_0) # Specify the IVP conditions

# Run the simulation
print(flush=True) # Flush the buffer before the progress bar starts
with tqdm(total=len(time_steps_s), desc="Running Simulation") as pbar: # Create a progress bar manually
    ts_index = 1 # Current time-step index
    pbar.update() # Since we start one time step in
    
    while (rk4.successful() and rk4.t <= c.T_F and ts_index < len(time_steps_s)):
        # Multiple checks to verify validity of integration process
        
        # Calculate voltages on op-amp inputs (using last voltage) and op-amp output
        invert_inp_V[ts_index] = c.VREF + (cap_charge_C[ts_index - 1] / c.C)
        ninvrt_inp_V[ts_index] = c.VREF + ((output_volts[ts_index - 1] - c.VREF) * c.R2 / (c.R2 + c.R3))
        output_volts[ts_index] = op_amp(ninvrt_inp_V[ts_index], invert_inp_V[ts_index])
        
        rk4.set_f_params(c, output_volts[ts_index]) # Set parameters for the differential eq.
        rk4.integrate(time_steps_s[ts_index]) # Run the numerical integration
        cap_charge_C[ts_index] = rk4.y[0]   # Extract capacitor charge from the integrator
        
        ts_index += 1   # Move on to the next time step
        pbar.update()
print(flush=True) # Flush the buffer after completing too

''' ===== Plot/Output Section ===== '''

# Compute information about the oscillation charactaristics of the circuit
f_Hz, T_s, duty_cycle, t_high, t_low = computeFrequencyParams(c)

print(f"\nThe circuit oscillates with a frequency of {f_Hz:.3f} Hz (Period = {T_s:.3f} s).")
print(f"The duty cycle is {duty_cycle:.1%} ({t_high:.3f} s high / {t_low:.3f} s low).")

plt.ion()   # Enable interactive mode
fig1 = plt.figure() # Create a graph figure for manual control

ax1 = fig1.add_axes((0.1, 0.22, 0.8, 0.7)) # Space for the legend, etc

# Plot the values on the left voltage axis
ax1.set_xlabel('Time, seconds')
ax1.set_ylabel('Volts', color='tab:blue')
ax1.plot(time_steps_s, reference_V, ':', label='Voltage Reference [V]', color='tab:gray', alpha=0.5)
ax1.plot(time_steps_s, output_volts, '-', label='Output [V]', color='tab:purple', alpha=0.75)
ax1.plot(time_steps_s, ninvrt_inp_V, '--', label='Non-inverting input [V]', color='tab:green')
ax1.plot(time_steps_s, invert_inp_V, '-', label='Inverting input [V]', color='tab:blue')
plt.yticks(np.linspace(np.floor(c.VEE), np.ceil(c.VCC), int(np.ceil(c.VCC) - np.floor(c.VEE)) + 1))
plt.grid(ls='--', lw=0.5)
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx() # Create graph with twinned x-axis

# Plot the charge on the capacitor on the right axis
ax2.set_ylabel('Capacitor Charge, Coulombs', color='tab:orange')
ax2.plot(time_steps_s, cap_charge_C, '-.', label='Capacitor Charge [C]', color='tab:orange', alpha=0.75)
ax2.tick_params(axis='y', labelcolor='tab:orange')

plt.title("Simulation Data vs. Time")

# Add a legend to the bottom of the figure using bbox_to_anchor
fig1.legend(ncol=3, loc="upper right", bbox_to_anchor=(0., 0.02, 1., 0.1), mode="expand")

plt.show()

# plt.draw()  # Non-blocking
# plt.pause(1) # Sleep main script to give figure time to draw
# # See https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib

# # ninv_inputs = np.linspace(c.VDD, c.VCC) # input voltages to non-inverting input
# # outputs = np.zeros_like(ninv_inputs)

# # for index in range(len(ninv_inputs)):
# #     outputs[index] = op_amp(ninv_inputs[index], c.VCC / 2)
    
# # plt.plot(ninv_inputs, outputs)


''' ===== Data File Output Section ===== '''

# Columnate data into a single numpy array for CSV output
columnated = np.column_stack((time_steps_s, reference_V, output_volts,
                             ninvrt_inp_V, invert_inp_V, cap_charge_C))
np.savetxt('output.csv', columnated, delimiter=', ', comments='', fmt='%e',
           header='Time [s], Reference [V], Output [V], Non-Inverting Input [V], Inverting Input [V], Capacitor Charge [C]',)


# while inval == 3: # Ask user if they want to save the constants if they manually entered them
#     instr = input("Do you want to save these constants to a file? y/[n] -> ").lower()
#     try:
#         if instr == 'y':
#             raise NotImplementedError("Not implemented yet")
#             break
#         elif instr == 'n' or instr == '':
#             break
#         else:
#             raise ValueError("Please enter only 'y' or 'n' or leave blank")
#     except (ValueError, NotImplementedError) as e:
#         print(f"Error: {e}")

# input(":")        
        
# ''' Ensure figure won't close '''
# plt.show()
