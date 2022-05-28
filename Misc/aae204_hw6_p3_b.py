import numpy as np
import matplotlib.pyplot as plt

L1 = 15 # in
L2 = 8 # in

l = 1 / np.sqrt(3) # in
L = L1 - l # in

T = 30 # kip-in
G = 5.94e3 # ksi

x = np.linspace(0, L1 + L2, 20000) # in
gam = np.empty_like(x)

s1 = x < L
s2 = (x > L) & (x < 15)
s3 = x > 15

gam[s1] = T * 2.5 / (G * np.pi / 32. * (5.**4 - 2.**4))
gam[s2] = T * 2.5 / (G * np.pi / 32. * (5.**4 - (2. - 2. * (x[s2] - L) / l)**4))
gam[s3] = T * 1.5 / (G * np.pi / 32. * (3.**4))

plt.plot(x, gam * 10.**6)
plt.xlabel(r"Position Along Rod $x$ [in]")
plt.ylabel(r"Maxium Shear Strain $\gamma$ [μradians]")
plt.title("Maximum Shear Strain vs. Position")
plt.ylim(0, 1000)
plt.xlim(0, L1 + L2)
plt.grid(True)
plt.show()
