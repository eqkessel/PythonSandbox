# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:52:03 2020

@author: redne
"""

# One-liner
from functools import reduce; print(sum(map(len , map(lambda l : reduce(lambda x, y : set(x) & set(y), l), map(lambda item : item.split(), open("input.txt").read().split('\n\n'))))))

# from functools import reduce

# with open("input.txt") as inp_raw:
#     groups = list(map(lambda item : item.split(), inp_raw.read().split('\n\n')))
#     questions = list(map(lambda ls : reduce(lambda x, y : set(x) & set(y), ls), groups))
#     pt2 = sum(map(lambda group : len(group), questions))
#     print(f"Part 2: {pt2}")