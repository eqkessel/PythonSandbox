# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 22:53:27 2020

@author: redne
"""
from copy import deepcopy

with open("input.txt") as file:
    raw = file.read()
    
    orig_instrs = list(map(lambda s : [s, 0], raw.split('\n')))[:-1]
    
    for instr_addr in range(len(orig_instrs)):
        # Reset code
        instrs = deepcopy(orig_instrs)
        acc = 0
        instr_ptr = 0
        
        if instrs[instr_addr][0][:3] == 'acc':
            continue
        elif instrs[instr_addr][0][:3] == 'nop':
            print(f"changing instruction at address {instr_addr} to jmp")
            instrs[instr_addr][0] = instrs[instr_addr][0].replace('nop', 'jmp')
        elif instrs[instr_addr][0][:3] == 'jmp':
            print(f"changing instruction at address {instr_addr} to nop")
            instrs[instr_addr][0] = instrs[instr_addr][0].replace('jmp', 'nop')

        while instr_ptr < len(orig_instrs) and instrs[instr_ptr][1] < 1:
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
            
        if instr_ptr == len(orig_instrs):
            print(f"code reached end of sequence ({instr_ptr})")
            break
        else:
            print(f"code attempted to re-execute instruction {instr_ptr}")
        
    print(acc)