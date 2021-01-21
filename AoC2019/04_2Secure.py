# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 22:01:29 2019

@author: redne
"""

lo = 146810
hi = 612564

codes = []
count = 0

for num in range(lo, hi + 1):
    passcode = str(num)
    lastDigit = 0
    pot_double = False
    double = False
    chain = 0
    decreasing = True
    for n in passcode:
        currDigit = int(n)
        if (currDigit < lastDigit):     # Password has a decreasing value
            decreasing = False
            break
        # Password has a doubled digit
        elif (currDigit == lastDigit):  
            chain += 1
            if (chain == 2):    # Exactly 2 long (currently)
                pot_double = True
            elif (chain > 2):   # Longer than 2
                pot_double = False
        else:                           # Password digit increases 
            if (pot_double):
                double = True
                pot_double = False
            chain = 1
            lastDigit = currDigit
    if ((double or pot_double) and decreasing):
        #print(num)
        codes.append(num)
        count += 1
        
print(len(codes))
