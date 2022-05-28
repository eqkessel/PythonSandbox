import matplotlib.pyplot as plt
import numpy as np

def tri(x):
    return np.arcsin(np.sin(x)) / (np.pi / 2)

t = np.linspace(0, 0.002, 2000)
v_out = (4/9)*2.25 + (4/9)*(4.5*tri(2 * np.pi *1000 * t)) + (1/18)*(3.6*np.sin(2 * np.pi *10000 * t))

plt.plot(t, v_out)
plt.grid()
plt.xlabel("time [s]")
plt.ylabel("V_out [V]")
plt.title("Output Voltage vs. Time")
plt.show()
