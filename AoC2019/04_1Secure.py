# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:01:29 2019

@author: redne
"""

lo = 146810
hi = 612564

codes = []

for num in range(lo, hi + 1):
    passcode = str(num)
    lastDigit = 0
    double = False
    decreasing = True
    for n in passcode:
        currDigit = int(n)
        if (currDigit < lastDigit):     # Password has a decreasing value
            decreasing = False
            break
        elif (currDigit == lastDigit):  # Password has a doubled digit
            double = True
        else:                           # Password digit increases 
            lastDigit = currDigit
    if (double and decreasing):
        codes.append(num)
        
print(len(codes))