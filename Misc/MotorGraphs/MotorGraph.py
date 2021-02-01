import os
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D # Needed for 3D plotting

# load in CSV data

fpath = os.path.dirname(os.path.abspath(__file__))

voltages = [12, 10, 8, 6, 4]

data = []

for voltage in voltages:
    fname = os.path.join(fpath, f"MotorCurve-{voltage}V.csv")
    data.append(np.loadtxt(fname, skiprows=1, delimiter=','))

# massage data
data.append(np.zeros_like(data[0])) # Add an extrapolated zero-value to the measurements
voltages.append(0)  # And the the voltages they occured at

data = np.array(data)

# mesh_volts, mesh_speed = np.meshgrid(voltages, data[:,:,0])
mesh_volts = np.tile(voltages, (data.shape[1], 1)).T

# plot data

fig = plt.figure()
ax0 = fig.add_subplot(221, projection='3d')
ax0.plot_surface(data[:,:,0], mesh_volts, data[:,:,1], alpha=0.5, color=(0.8, 0.7, 0.0))
ax0.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,1], rstride=1, cstride=25, color=(0.8, 0.7, 0.0))

ax0.set_xlabel('Shaft Speed (RPM)')
ax0.set_ylabel('Input Voltage (V)')
ax0.set_zlabel('Torque Output (N-m)')
ax0.set_title('Torque Charactaristics')

ax1 = fig.add_subplot(222, projection='3d')
ax1.plot_surface(data[:,:,0], mesh_volts, data[:,:,3], alpha=0.5)
ax1.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,3], rstride=1, cstride=25, linestyles='dotted')
ax1.plot_surface(data[:,:,0], mesh_volts, data[:,:,4], alpha=0.5, color=(0.0, 0.8, 0.2))
ax1.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,4], rstride=1, cstride=25, linestyles='solid', color=(0.0, 0.8, 0.2))
ax1.plot_surface(data[:,:,0], mesh_volts, data[:,:,6], alpha=0.5, color=(0.8, 0.6, 0.0))
ax1.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,6], rstride=1, cstride=25, linestyles='dashed', color=(0.8, 0.6, 0.0))

ax1.set_xlabel('Shaft Speed (RPM)')
ax1.set_ylabel('Input Voltage (V)')
ax1.set_zlabel('Power (W)')
ax1.set_title('Power Charactaristics')

ax2 = fig.add_subplot(223, projection='3d')
ax2.plot_surface(data[:,:,0], mesh_volts, data[:,:,2], alpha=0.5)
ax2.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,2], rstride=1, cstride=25)

ax2.set_xlabel('Shaft Speed (RPM)')
ax2.set_ylabel('Input Voltage (V)')
ax2.set_zlabel('Current (A)')
ax2.set_title('Current Charactaristics')

ax3 = fig.add_subplot(224, projection='3d')
ax3.plot_surface(data[:,:,0], mesh_volts, data[:,:,5], alpha=0.5)
ax3.plot_wireframe(data[:,:,0], mesh_volts, data[:,:,5], rstride=1, cstride=25)
ax3.set_zlim3d(0, 100)

ax3.set_xlabel('Shaft Speed (RPM)')
ax3.set_ylabel('Input Voltage (V)')
ax3.set_zlabel('Efficiency (%)')
ax3.set_title('Efficiency Charactaristics')

plt.show()
