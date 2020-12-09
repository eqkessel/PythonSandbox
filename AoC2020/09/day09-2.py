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
            break
        
    for slice_len in range(2, len(sequence) + 1):
        print(f"processing sub-sequences of length {slice_len}")
        for slice_start in range(len(sequence) - slice_len):
            seq_slice = sequence[slice_start : slice_start + slice_len]
            if sum(seq_slice) == number:
                weakness = min(seq_slice) + max(seq_slice)
                print(weakness)
                sys.exit()