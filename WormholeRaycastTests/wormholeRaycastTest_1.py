# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:33:46 2020

@author: redne
"""

vector_package_path = 'C:\\Users\\redne\\Documents\\Git\\PythonSandbox\\Vectors\\vector'
import sys

if (vector_package_path not in sys.path):
    sys.path.append(vector_package_path)

import vector as vec

from scipy.integrate import ode
import matplotlib.pyplot as plot
import numpy as np
import math as m
import scipy.constants as const

#print(str(vector.zeroVector()))

# WORMHOLE CONSTANTS

THROAT_DIA_m = 100
THROAT_LEN_m = 100
LENS_WIDTH_m = 25

MASS_PARAM = LENS_WIDTH_m / 1.42953

def r_func(l):
    # radius r as a function of radial distance l
    if (abs(l) > THROAT_LEN_m):
        if (MASS_PARAM > 0.0):
            x = 2 * (abs(l) - THROAT_LEN_m) / (const.pi * MASS_PARAM)
        
            r = THROAT_DIA_m + MASS_PARAM * (x * m.atan(x) - 0.5 * m.log(1 + x * x))
        else:
            r = THROAT_DIA_m + abs(l) - THROAT_LEN_m
    else:
        r = THROAT_DIA_m
    return r

def dr_dl(l):
    # r'(l) = dr/dl
    if (abs(l) > THROAT_LEN_m):
        if (MASS_PARAM > 0.0):
            # since r is originally defined as an integral with respect to |l|-a, we can use FTC
            # to easily compute its derivative. The bound of |l|-a complicates it, but the resulting
            # formula is sign(x)f(|x|-a)
            
            dr_dl = 2 / m.pi * m.copysign(1.0, l) * m.atan(2 * (abs(l) - THROAT_LEN_m) / (m.pi * MASS_PARAM))
        else:
            dr_dl = 1.0
    else:
        dr_dl = 0.0
    return dr_dl

# polar coords of camera relative to wormhole
cam_pos = vec.Vector(l = 2 * (THROAT_LEN_m + THROAT_DIA_m + LENS_WIDTH_m), theta = 0.0 * m.pi)
print("Camera position = {!r}".format(cam_pos))

# let a Cartesian corrdinate system exist at the camera w/ x along increasing l and y along increasing theta
# given an camera ray angle in this coordinate system, the reverse unit vector of the angle's corresponding
# vector is the ray of propogration, in terms of a radial component and an angular component
ray_ang = m.pi * 0.99
ray_n = vec.Vector(l = -m.cos(ray_ang), theta = -m.sin(ray_ang))
print("Ray propogation = {!r}".format(ray_n))

# compute cannonical momentum
ray_p = vec.Vector(l = ray_n['l'], theta = (r_func(cam_pos['l']) * ray_n['theta']))
print("Ray momentum = {!r}".format(ray_p))

# compute motion constants
#b = ray_p['theta']
#B_2 = b ** 2
# these just simplify to angular momentum ptheta in 2d

# set up initial state vector and data arrays
s0 = [cam_pos['l'],         # l, radial pos
      cam_pos['theta'],     # theta, angular pos
      ray_p['l'],           # pl, radial momentum component
      ray_p['theta']        # ptheta, angular momentum component
      ]

t_end = 0.0
t_start = -1000.0
dt = -0.1

ts = np.arange(t_end, t_start, dt)  # run time backwards to trace ray
l       = np.zeros(len(ts))
theta   = np.zeros(len(ts))
pl      = np.zeros(len(ts))
ptheta  = np.zeros(len(ts))
r       = np.zeros(len(ts))
l[0]        = s0[0]
theta[0]    = s0[1]
pl[0]       = s0[2]
ptheta[0]   = s0[3]
r[0]        = r_func(s0[0])

# Differential system
def f(t, s):
    _r      = r_func(s[0])  # compute r from l
    _dr_dl  = dr_dl(s[0])   # compute dr/dl from l
    
    dl      = s[2]              # pl
    dtheta  = s[3] / (_r ** 2)  # ptheta / r^2
    dpl     = (s[3] ** 2) * _dr_dl / (_r ** 3)  # ptheta^2 * dr/dl / r^3
    dptheta = 0                 # angular momentum is constant
    
    return [dl,
            dtheta,
            dpl,
            dptheta]

# set up and run the integrator
myInt = ode(f).set_integrator('dopri5')
myInt.set_initial_value(s0, t_end)    

i = 1
while (myInt.successful() and myInt.t > t_start and i < len(ts)):
    myInt.integrate(myInt.t + dt)
    l[i]        = myInt.y[0]
    theta[i]    = myInt.y[1]
    pl[i]       = myInt.y[2]
    ptheta[i]   = myInt.y[3]
    r[i]        = r_func(myInt.y[0])
    i = i + 1
#print(i)
    
# plot stuff
plot.figure(1)
plot.cla()
plot.grid()
plot.plot(r[0:i] * np.cos(theta[0:i]), r[0:i] * np.sin(theta[0:i]))

'''
# set up 2d Cartesian coords w/ x along increasing l and y along increasing theta
cam_Cartesian_x = vec.Vector(math.cos(cam_pos['theta']),\
                             math.copysign(1.0,cam_pos['l']) * math.sin(cam_pos['theta']))
cam_Cartesian_y = vec.Vector(-cam_Cartesian_x['j'], cam_Cartesian_x['i'])
    
print("Cartesian x = {}".format(cam_Cartesian_x))
print("Cartesian y = {}".format(cam_Cartesian_y))

# pick an orientation of ray leaving camera in this camera
cam_ray_angle = math.pi * 0.75   # slightly backwards, towards wormhole (from + end)

# get the vector of the camera ray and negate to get the ray of propogation
cam_ray_n = -((math.cos(cam_ray_angle) * cam_Cartesian_x) + (math.sin(cam_ray_angle) * cam_Cartesian_y))

print("Camera ray propogration = {}".format(cam_ray_n))

# compute ray's canonical momentum
cam_ray_p = vec.Vector(l = )
'''