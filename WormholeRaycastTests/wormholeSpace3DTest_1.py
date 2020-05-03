# -*- coding: utf-8 -*-
"""
Created on Sun May  3 13:23:09 2020

@author: redne
"""

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

# Generate space curves
space_l     = np.linspace(-500, 500, 100)
space_theta = np.linspace(-m.pi, m.pi, 100)

# vectorize r and z functions so that they can be applied to l
vec_r_fn = np.vectorize(r_func)
vec_z_fn = np.vectorize(z_func)

# knit a mesh grid for plotting in terms of (l, theta)
mesh_l, mesh_theta = np.meshgrid(space_l, space_theta)

# apply r and z to new knitted l
mesh_r = vec_r_fn(mesh_l)
mesh_z = vec_z_fn(mesh_l)

# set up the 3D plot
fig = plot.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(mesh_r * np.cos(mesh_theta), mesh_r * np.sin(mesh_theta), mesh_z, alpha = 0.5)

#space_r = vec_r_fn(space_l)
#space_z = vec_z_fn(space_l)

# divide into a (+) side and a (-) side
#r_pos = np.copy(space_r)
#r_neg = np.copy(space_r)
#z_pos = np.copy(space_z)
#z_neg = np.copy(space_z)

#r_pos[space_l <= 0] = np.nan
#r_neg[space_l >= 0] = np.nan
#z_pos[space_l <= 0] = np.nan
#z_neg[space_l >= 0] = np.nan

# knit a mesh grid for plotting in terms of plot domain (theta, r)
#pl_r_pos, pl_theta_pos = np.meshgrid(r_pos, space_theta)
#pl_r_neg, pl_theta_neg = np.meshgrid(r_neg, space_theta)

# set up the 3D plot
# fig = plot.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_surface(pl_r_pos * np.cos(pl_theta_pos), pl_r_pos * np.sin(pl_theta_pos), z_pos, alpha = 0.5)

