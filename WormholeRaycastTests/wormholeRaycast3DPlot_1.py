# -*- coding: utf-8 -*-
"""
Created on Sun May  3 13:23:09 2020

@author: redne
"""

vector_package_path = 'C:\\Users\\redne\\Documents\\Git\\PythonSandbox\\Vectors\\vector'
import sys

if (vector_package_path not in sys.path):
    sys.path.append(vector_package_path)

import vector as vec

import matplotlib.pyplot as plot
import numpy as np
import math as m

from scipy.integrate import quad, ode # Numerical integrators

from mpl_toolkits.mplot3d import Axes3D # Activates 3D ploting, not referenced


# Wormhole parameters & functions
THROAT_DIA_m = 100
THROAT_LEN_m = 100
LENS_WIDTH_m = 100

MASS_PARAM = LENS_WIDTH_m / 1.42953

def r_func(l):
    # radius r as a function of radial distance l
    if (abs(l) > THROAT_LEN_m):
        if (MASS_PARAM > 0.0):
            x = 2 * (abs(l) - THROAT_LEN_m) / (m.pi * MASS_PARAM)
        
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

def z_func(l):
    # height of embeding diagram z as a function of radial distance l
    integrand = lambda x: m.sqrt(1 - (dr_dl(x) ** 2))
    intResult, err = quad(integrand, 0, l)  # integral 0->l of above function
    return intResult

# EMBEDING DIAGRAM
# Generate space curves
space_l     = np.linspace(-500, 500, 25)
space_theta = np.linspace(-m.pi, m.pi, 16)

# vectorize r and z functions so that they can be applied to l
vec_r_fn = np.vectorize(r_func)
vec_z_fn = np.vectorize(z_func)

# knit a mesh grid for plotting in terms of (l, theta)
mesh_l, mesh_theta = np.meshgrid(space_l, space_theta)

# apply r and z to new knitted l
mesh_r = vec_r_fn(mesh_l)
mesh_z = vec_z_fn(mesh_l)

# split into +l and -l halves
mesh_r_pos = np.copy(mesh_r)
mesh_r_neg = np.copy(mesh_r)
mesh_z_pos = np.copy(mesh_z)
mesh_z_neg = np.copy(mesh_z)

mesh_r_pos[mesh_l < 0] = np.nan
mesh_r_neg[mesh_l > 0] = np.nan
mesh_z_pos[mesh_l < 0] = np.nan
mesh_z_neg[mesh_l > 0] = np.nan

# RAY
# polar coords of camera relative to wormhole
cam_pos = vec.Vector(l = 1.5 * (THROAT_LEN_m + THROAT_DIA_m + LENS_WIDTH_m), theta = 0.0 * m.pi)
print("Camera position = {!r}".format(cam_pos))

# let a Cartesian corrdinate system exist at the camera w/ x along increasing l and y along increasing theta
# given an camera ray angle in this coordinate system, the reverse unit vector of the angle's corresponding
# vector is the ray of propogration, in terms of a radial component and an angular component
ray_ang = m.pi * 0.98
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
z       = np.zeros(len(ts))
l[0]        = s0[0]
theta[0]    = s0[1]
pl[0]       = s0[2]
ptheta[0]   = s0[3]
r[0]        = r_func(s0[0])
z[0]        = z_func(s0[0])

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
    z[i]        = z_func(myInt.y[0])
    i = i + 1
#print(i)
    
# plot stuff
# fig = plot.figure()
# ax = fig.add_subplot(111, projection='polar')
# c = ax.plot(theta[0:i], r[0:i])

# split into +l and -l halves
r_pos = np.copy(r)
r_neg = np.copy(r)
z_pos = np.copy(z)
z_neg = np.copy(z)
l_pos = np.copy(l)
l_neg = -np.copy(l)

r_pos[l < 0] = np.nan
r_neg[l > 0] = np.nan
z_pos[l < 0] = np.nan
z_neg[l > 0] = np.nan
l_pos[l < 0] = np.nan
l_neg[l > 0] = np.nan
# pos_side = theta.copy()
# neg_side = theta.copy()

# pos_side[l <= 0] = np.nan
# neg_side[l >= 0] = np.nan

# set up the 3D plot
fig = plot.figure()
#ax = fig.add_subplot(111, projection='3d')
graph_3d = fig.add_subplot(131, projection='3d')
graph_polar = fig.add_subplot(132, projection='polar')
graph_l = fig.add_subplot(133, projection='polar')

#ax.plot_surface(mesh_r * np.cos(mesh_theta), mesh_r * np.sin(mesh_theta), mesh_z, alpha = 0.5)

# plot embeding diagram space surface
graph_3d.plot_surface(mesh_r_pos * np.cos(mesh_theta), mesh_r_pos * np.sin(mesh_theta), mesh_z_pos, alpha = 0.2, color = 'g')
graph_3d.plot_surface(mesh_r_neg * np.cos(mesh_theta), mesh_r_neg * np.sin(mesh_theta), mesh_z_neg, alpha = 0.2, color = 'r')

# plot ray path
graph_3d.plot(r_pos[0:i] * np.cos(theta[0:i]), r_pos[0:i] * np.sin(theta[0:i]), z_pos[0:i], color = 'g')
graph_3d.plot(r_neg[0:i] * np.cos(theta[0:i]), r_neg[0:i] * np.sin(theta[0:i]), z_neg[0:i], color = 'r')

graph_polar.plot(theta[0:i], r_pos[0:i], color = 'g')
graph_polar.plot(theta[0:i], r_neg[0:i], color = 'r')

graph_l.plot(theta[0:i], l_pos[0:i], color = 'g')
graph_l.plot(theta[0:i], l_neg[0:i], color = 'r')

plot.show(block = True)