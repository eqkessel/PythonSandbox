import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

def Binet(n):
    return ((const.golden ** n) - ((-1 / const.golden) ** n)) / np.sqrt(5)

vec_Binet = np.vectorize(Binet, otypes=[complex])

real_limit = 8
imag_limit = 1.25
steps = 101

domain_real = np.linspace(-0, real_limit, steps)
domain_imag = np.linspace(complex(0, -imag_limit), complex(0, imag_limit), steps)

mesh_real, mesh_imag = np.meshgrid(domain_real, domain_imag)

domain_complex = mesh_real + mesh_imag

Fibonacci = vec_Binet(domain_complex)

real = Fibonacci.real
imag = Fibonacci.imag
magnitude = abs(Fibonacci)
phase_ang = np.angle(Fibonacci)

fig = plt.figure()

real_stride = round(float(steps) / float(real_limit * 1))
imag_stride = round(float(steps) / float(imag_limit * 2))

# ax1 = fig.add_subplot(221, projection='3d')
# ax1.plot_surface(mesh_real, mesh_imag.imag, real, alpha=0.3)
# ax1.plot_wireframe(mesh_real, mesh_imag.imag, real, rstride=real_stride, cstride=imag_stride)
# ax1.set_xlabel('Real')
# ax1.set_ylabel('Imaginary')
# ax1.set_zlabel('Real')

# ax2 = fig.add_subplot(223, projection='3d')
# ax2.plot_surface(mesh_real, mesh_imag.imag, imag, alpha=0.3)
# ax2.plot_wireframe(mesh_real, mesh_imag.imag, imag, rstride=real_stride, cstride=imag_stride)
# ax2.set_xlabel('Real')
# ax2.set_ylabel('Imaginary')
# ax2.set_zlabel('Imaginary')

ax3 = fig.add_subplot(111, projection='3d')
ax3.plot_surface(real, mesh_imag.imag, imag, alpha=0.3)
ax3.plot_wireframe(real, mesh_imag.imag, imag, rstride=real_stride, cstride=imag_stride)
ax3.set_xlabel('Binet Formula Real')
ax3.set_ylabel('Imaginary Input')
ax3.set_zlabel('Binet Formula Imaginary')

plt.show()