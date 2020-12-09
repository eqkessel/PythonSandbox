# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:48:01 2020

@author: redne
"""

def search_1(sequence, number):
    print(" PROCESSING METHOD 1")
    iters = 1
    for slice_len in range(2, len(sequence) + 1):
        print(f"processing sub-sequences of length {slice_len}")
        for slice_start in range(len(sequence) - slice_len):
            seq_slice = sequence[slice_start : slice_start + slice_len]
            if sum(seq_slice) == number:
                weakness = min(seq_slice) + max(seq_slice)
                return weakness, iters
            iters += 1

def search_2(sequence, number):
    print(" PROCESSING METHOD 2")
    iters = 1
    for start in range(len(sequence) - 1):
        # print(f"processing sub-sequences starting at {start}") # Too spammy
        end = start + 2
        while end <= len(sequence):
            seq_slice = sequence[start : end]
            if sum(seq_slice) == number:
                weakness = min(seq_slice) + max(seq_slice)
                return weakness, iters
            end += 1
            iters += 1

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
        
    m1 = search_1(sequence, number)
    m2 = search_2(sequence, number)
    
    print(f"METHOD 1: {m1}\nMETHOD 2: {m2}")
        
    