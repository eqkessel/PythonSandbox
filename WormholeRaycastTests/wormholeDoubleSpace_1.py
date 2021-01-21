'''
wormholeDoubleSpace_1.py

Testing having wormhole entrance and exit on the same Cartesian plane.

May 2020 Ethan K.
'''

vector_package_path = 'C:\\Users\\redne\\Documents\\Git\\PythonSandbox\\Vectors\\vector'
import sys

if (vector_package_path not in sys.path):
    sys.path.append(vector_package_path)

import vector as vec

import numpy as np
import math as m

class Wormhole:
    def __init__(self, posCoord, posAngle, negCoord, negAngle, throatRadius, throatLength, lensWidth):
        self.posCoord   = posCoord  # Cartesian position of positive side
        self.negCoord   = negCoord  # " negative side
        self.posAngle   = posAngle  # polar 0 angular offset from cartesian x-axis for positive side
        self.negAngle   = negAngle  # " negative side
        self.throatRadius   = throatRadius  # radius of wormhole throat section
        self.throatLength   = throatLength  # length of wormhole throat section
        self.lensWidth      = lensWidth     # effective lensing width

    def massParam(self):
        return self.lensWidth * 0.6995306

    def cartesianToPolar(self, cartesianCoord):
        posDelta = cartesianCoord - self.posCoord
        negDelta = cartesianCoord - self.negCoord
        posDist = abs(posDelta)
        negDist = abs(negDelta)

        if (posDist <= negDist):
            _l = posDist
            _theta = vec.angle(posDelta) - self.posAngle
        else:
            _l = -negDist
            _theta = vec.angle(posDelta) - self.negAngle

        return vec.Vector(l = _l, theta = _theta)
    
    def r_func(self, l):
        # radius r as a function of radial distance l
        m_param = self.massParam()
        if (abs(l) > self.throatLength):
            if (m_param > 0.0):
                x = 2 * (abs(l) - self.throatLength) / (m.pi * m_param)
            
                r = self.throatRadius + m_param * (x * m.atan(x) - 0.5 * m.log(1 + x * x))
            else:
                r = self.throatRadius + abs(l) - self.throatLength
        else:
            r = self.throatRadius
        return r

    def dr_dl(self, l):
        # r'(l) = dr/dl
        m_param = self.massParam()
        if (abs(l) > self.throatLength):
            if (m_param > 0.0):
                # since r is originally defined as an integral from 0 to |l|-x, we can use the FTC
                # to compute its derivative with respect to l. The bound of |l|-x complicates using
                # FTC "normally" where F'(l) = f(l) given F(l) = int [a -> l] (f(t) dt)
                # but the resulting formula is sign(l)*f(|l|-x). Proof of this pending, works experimentally.
                
                dr_dl = 2 / m.pi * m.copysign(1.0, l) * m.atan(2 * (abs(l) - self.throatLength) / (m.pi * m_param))
            else:
                dr_dl = 1.0
        else:
            dr_dl = 0.0
        return dr_dl
