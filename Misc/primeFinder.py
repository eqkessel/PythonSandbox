# -*- coding: utf-8 -*-
"""
Created on Wed May 20 20:52:15 2020

@author: redne
"""

numbers = {0: False,
           1: False,
           2: True}

primes = [2]

num = 3

check_until = 5000

def checkPrime(n):
    for factor in primes:
        if (n % factor == 0):
            return False
    
    primes.append(n)
    return True

while (num <= check_until):
    numbers[num] = checkPrime(num)
    num += 1
    
def getFactorization(n):
    if (n in primes):
        return {n : 1}
    factors = {}
    remaining = n
    while (remaining not in primes):
        factorFound = False
        for factor in primes:
            if (remaining % factor == 0):
                factors[factor] = factors.get(factor, 0) + 1
                remaining = int(remaining / factor)
                factorFound = True
                break
        if (not factorFound):
            raise ValueError('remaining value ({}) neither prime nor factorable in current list'.format(remaining))
    factors[remaining] = factors.get(remaining, 0) + 1
        
    return factors

def recursivelyFactor(n, *, lowerLimit = 2):
    print('now factoring: {}'.format(n))
    factors = {}
    factor = lowerLimit
    upperLimit = int(n/2)
    
    factorFound = False
    while (factor <= upperLimit):
        if (n % factor == 0):
            factors[factor] = factors.get(factor, 0) + 1
            remaining = int(n / factor)
            print('    {0} factors into {1} and {2}'.format(n, factor, remaining))
            
            subFactors = recursivelyFactor(remaining, lowerLimit = factor)
            
            for key in subFactors.keys():
                factors[key] = factors.get(key, 0) + subFactors[key]
            
            factorFound = True
            break    
        factor += 1
    
    if (not factorFound):
        factors[n] = factors.get(n, 0) + 1
    #factors[remaining] = factors.get(remaining, 0) + 1    
    
    return factors

print(recursivelyFactor(12345678987654321))