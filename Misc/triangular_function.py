import matplotlib.pyplot as plt
import numpy as np

def tri(x):
    return np.arcsin(np.sin(x)) / (np.pi / 2)

x = np.linspace(0, 0.002, 200)
y = 3 * tri(2 * np.pi * 1000 * x) + 1

plt.plot(x, y)
plt.grid(True)
plt.xlabel("$t$ [sec]")
plt.ylabel("$3$tri$(2\pi1000t)+1$ [V]")
plt.title("Triangular Signal Example")
plt.show()
