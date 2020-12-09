# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:48:01 2020

@author: redne
"""

import sys

with open("input.txt") as file:
    raw_inp = file.read()
    
    sequence = list(map(int, raw_inp.split()))
    
    for target_index in range(25, len(sequence)):
        number = sequence[target_index]
        seq_slice = sequence[target_index - 25 : target_index]
        
        if not any(map(lambda val : (number - val in seq_slice) and (number - val != val), seq_slice)):
            print(number)
            sys.exit()
        
        # for value in seq_slice:
        #     addend = number - value
        #     if addend not in seq_slice or addend == value:
        #         print(number)
        #         sys.exit()