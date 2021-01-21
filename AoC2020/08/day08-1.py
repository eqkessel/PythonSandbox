# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 22:53:27 2020

@author: redne
"""

with open("input.txt") as file:
    raw = file.read()
    
    instrs = list(map(lambda s : [s, 0], raw.split('\n')))
    
    acc = 0
    instr_ptr = 0
    
    while instrs[instr_ptr][1] < 1:
        instrs[instr_ptr][1] += 1
        opcode, arg = instrs[instr_ptr][0].split()
        arg = int(arg)
        
        if opcode == 'nop':
            ptr_change = 1
        elif opcode == 'acc':
            acc += arg
            ptr_change = 1
        elif opcode == 'jmp':
            ptr_change = arg
            
        instr_ptr += ptr_change
        
    print(acc)