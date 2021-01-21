# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:52:03 2020

@author: redne
"""

with open("input.txt") as inp_raw:
    groups = list(map(lambda item : set(item.replace('\n','')), inp_raw.read().split('\n\n')))
    pt1 = sum(map(lambda group : len(group), groups))
    print(f"Part 1: {pt1}")