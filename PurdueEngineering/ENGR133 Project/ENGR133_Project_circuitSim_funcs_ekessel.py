#******************************************************************************
#
# ENGR 133 - FA 20 - LC4-02
# Personal Project - Ethan Kessel (ekessel@purdue.edu)
#
# ENGR133_Project_circuitSim_funcs_ekessel.py
#
# This file contains some of the functions for the main script.
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

# Convert decibels to unitless voltage amplification
def dBtoAmp(decibels): return (10 ** (decibels / 20))

# Uses a lambda to create a function that behaves like an op-amp
def makeOpAmpFunc(gain, vcc, vdd = 0):
    if vcc <= vdd:
        raise ValueError("Vcc must have a higher potential than Vdd")
    return lambda ninv, inv : (np.clip((gain * (ninv - inv) + (vcc + vdd) / 2), vdd, vcc))
