
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import default_rng
import matplotlib.ticker as plticker
from scipy.optimize import least_squares

SAMPLE_SEPARATION__DEG = 30.
ANGLE_ERROR = 0.2

AMPLITUDE = 2.3
PHASE__DEG = 15.
OFFSET = 3.
NOISE = 0.05

rng = default_rng(12345)

x = np.arange(-90. + SAMPLE_SEPARATION__DEG, 90., SAMPLE_SEPARATION__DEG)
x += rng.standard_normal(x.shape) * SAMPLE_SEPARATION__DEG * ANGLE_ERROR

x = np.concatenate(([-90.], x, [90.]))

xs = np.linspace(-90., 90.)

def f(x, a, b, c):
    return a * np.sin(2 * np.deg2rad(x) + np.deg2rad(b)) + c

y = f(x, AMPLITUDE, PHASE__DEG, OFFSET)
y += rng.standard_normal(y.shape) * AMPLITUDE * NOISE

ys = f(xs, AMPLITUDE, PHASE__DEG, OFFSET)

def residuals(b):
    return f(x, *b) - y

result = least_squares(residuals, (1, 0, 1), bounds=((0, -90., 0),(np.inf, 90., np.inf)))

y_predict = f(xs, *result.x)

fig, ax = plt.subplots(1,1)

ax.plot(x, y, 'dg')
ax.plot(xs, ys, '--k')
ax.plot(xs, y_predict, ':r')

ax.set_xlim(-90., 90.)
ax.xaxis.set_major_locator(plticker.MultipleLocator(base=15.0))

ax.grid()

plt.show()
