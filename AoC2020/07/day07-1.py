# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 22:32:33 2020

@author: redne
"""

target_color = 'shiny gold'

def removeStrings(in_string, string_iter):
    out_string = in_string
    for sub_string in string_iter:
        out_string = out_string.replace(sub_string, '')
    return out_string

def searchBags(target_color, rules_clean, ext_bags):
    for color in rules_clean:
        if target_color in rules_clean[color]:
            ext_bags.update({color:None})
            searchBags(color, rules_clean, ext_bags)
            

with open("input.txt") as inp_raw:
    rules = inp_raw.read().split('\n')[:-1] # Last item is empty, discard
    
    rules_clean = {}
    
    for line in rules:
        sp_ln = removeStrings(line, (' contain', ' no other bags', ' bags', ' bag')).split()
        outer1, outer2, *other = map(lambda item: item.strip(' ,.'), sp_ln) # Remove extraneous characters
        outer_name = f"{outer1} {outer2}"
        rules_clean[outer_name] = {}
        for index in range(0, len(other), 3):
            num, inner1, inner2 = other[index : index+3]
            inner_name = f"{inner1} {inner2}"
            rules_clean[outer_name][inner_name] = int(num)
            
    ext_bags = {}
    
    searchBags(target_color, rules_clean, ext_bags)
    
    print(len(ext_bags))