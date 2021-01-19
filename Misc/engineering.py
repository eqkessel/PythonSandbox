# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:34:45 2020

@author: redne
"""

import numpy as np
import matplotlib.pyplot as plt

horiz = np.linspace(0, np.pi)

solve = (np.cos(horiz) + 1) / 2
make  = 1 - solve

plt.figure(figsize=(16, 8))
plt.stackplot(horiz, solve, make, colors=('blue', 'orange'), alpha=0.7)
plt.title("Time Spent Solving Problems and Time Spent Creating Problems vs." +\
          " Progress in an Engineering Career", pad=45, fontweight='bold')
plt.legend(["Time Spent Solving Problems", "Time Spent Creating Problems"],
           loc='lower center', ncol=2, bbox_to_anchor=(0., 1.02, 1., 1.02),
           borderaxespad=0.)   
tick_spots = np.array([0.0, 0.2, 0.5, 0.8, 1.0]) * np.pi

plt.xlabel("Progress in Engineering Career", labelpad=20)
plt.ylabel("Relative Percentage of Time Spent Engineering", labelpad=15)

plt.xticks(tick_spots, ["Engineering Student",
                        "Engineering Intern",
                        "Engineer",
                        "Senior Engineer",
                        "Engineering Manager"])
plt.yticks([0, 0.25, 0.5, 0.75, 1], ["0%",
                                     "25%",
                                     "50%",
                                     "75%",
                                     "100%"])
plt.grid(linestyle='-', axis='y')
plt.grid(linestyle=':', axis='x')
