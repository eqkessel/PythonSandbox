import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax1 = fig.add_subplot(221, projection='3d')
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(222)
ax4 = fig.add_subplot(224, projection='polar')


def Binet(n):
    return ((const.golden ** n) - ((-1 / const.golden) ** n)) / np.sqrt(5)

vec_Binet = np.vectorize(Binet, otypes=[complex])

domain = np.linspace(-4, 4, 200)

Fibonacci = vec_Binet(domain)
real = Fibonacci.real
imag = Fibonacci.imag
magnitude = abs(Fibonacci)
phase_ang = np.angle(Fibonacci)

ax1.plot(domain, real, imag)

ax2.plot(real, imag)

ax3.plot(domain, magnitude, label='magnitude')
ax3.plot(domain, phase_ang, label='phase angle')
ax3.legend()

ax4.plot(phase_ang, magnitude)

plt.show()