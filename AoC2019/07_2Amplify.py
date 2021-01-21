# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 23:09:51 2019

@author: redne
"""

import logging
import intcode.intcode as ic

from itertools import permutations
from tqdm import tqdm

logger = logging.getLogger('intcode')
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.WARNING)
stream.setFormatter(ic.logFormat)

if (logger.hasHandlers()):
    logger.removeHandler(stream)
logger.addHandler(stream)

phaseBase = '56789'
phases = [''.join(p) for p in permutations(phaseBase)]

nMachines = 5
code = input("Prgm:\n")

machines = [ic.Interpreter(code, aRunMode = ic.RunModes.UNTIL_OUTPUT) for n in range(nMachines)]

try:
    solutions = {}
    for pattern in tqdm(phases):
        out = 0
        for n in range(len(machines)):
            machines[n].reboot()
            machines[n].loadInput(int(pattern[n]))
        while True:
            for n in range(len(pattern)):
                machines[n].loadInput(out)
                machines[n].run()
                try:
                    out = machines[n].popOutput(0)
                except:
                    pass
            if (not machines[-1].running_):
                break
        solutions[pattern] = out
    
    print("**FINISHED EXECUTING, TESTING**")
    
    maximum = 0
    maxOption = ''
    for option in solutions.keys():
        outVal = solutions[option]
        if (outVal > maximum):
            maximum = outVal
            maxOption = option
            
    print("Option", maxOption, "gives", maximum)
    
finally:
    del machines
    logger.removeHandler(stream)