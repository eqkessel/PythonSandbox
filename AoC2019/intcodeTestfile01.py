# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:44:34 2019

@author: redne
"""

import logging
import intcode.intcode as ic

from itertools import permutations
from tqdm import tqdm

#print(dir(ic))
#print(dir(ic.Interpreter))

logger = logging.getLogger('intcode')
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.WARNING)
stream.setFormatter(ic.logFormat)

if (logger.hasHandlers()):
    logger.removeHandler(stream)
logger.addHandler(stream)

logger.info("This is an informative statement")
logger.debug("This is a test debug")
logger.warning("This is a test warning")
logger.error("This is a test error")
logger.critical("This is a test critical error")

#machines = [ic.Interpreter('99,0,0') for n in range(5)]
#print(machines)

phaseBase = '56789'
phases = [''.join(p) for p in permutations(phaseBase)]

nMachines = 5
code = input("Prgm:\n")
# 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

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
                phase = int(pattern[n])
                #machines[n].reboot()
                #machines[n].loadInput(phase)
                machines[n].loadInput(out)
                machines[n].run()
                try:
                    out = machines[n].popOutput(0)
                except:
                    pass
                    
        #        inputs.append(currPhase)
        #        inputs.append(out)
        #        runProgram(prgmIn)
        #        out = outputs.pop()[0]
                #print("Program outputed", out)
                #input("Waiting...")
            if (not machines[-1].running_):
                #print("EXITED LOOP")
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
    
    #del mach1
    
    #input("Waiting")
finally:
    del machines
    logger.removeHandler(stream)