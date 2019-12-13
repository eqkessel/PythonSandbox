# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 22:51:18 2019

@author: redne
"""

import math
import numpy as np

def zeroVector(nDims = 3):
    return Vector([0] * nDims)

def dotProd(vect1, vect2):
    # Dot product function - takes 2 vectors of the same size. Currently no component name checks
    if (not (isinstance(vect1, Vector) and isinstance(vect2, Vector))):
        raise TypeError("inputs to a dot product must both be vectors")
    if (len(vect1) != len(vect2)):
        raise ValueError("cannot dot two vectors of different size")
    return sum([a * b for a, b in zip(vect1, vect2)])

def crsProd(vect1, vect2):
    # Dot product function - takes 2 vectors of the same size. Currently no component name checks
    if (not (isinstance(vect1, Vector) and isinstance(vect2, Vector))):
        raise TypeError("inputs to a dot product must both be vectors")
    if (not (len(vect1) == len(vect2) == 3)):
        raise ValueError("can only cross two vectors in 3-space")
    """
    The easiest way to understand cross products is with the determinant of a matrix
    with their components:
            | i   j   k |
    a x b = | a1  a2  a3| = i(a2b3-a3b2)-j(a1b3-a3b1)+k(a1b2-a2b1)
            | b1  b2  b3|
    """
    a = tuple(vect1)
    b = tuple(vect2)
    i = a[1]*b[2] - a[2]*b[1]
    j = a[2]*b[0] - a[0]*b[2]
    k = a[0]*b[1] - a[1]*b[0]
    return Vector(i,j,k)

def normalize(vect):
    # Normalize a vector; i.e. make to have |v| = 1
    return vect / abs(vect)
    
class Vector:
    __unitComponents = 'ijk'
    
    def __checkNum(number):
        if (type(number) == float or type(number) == int):
            return number   # Number is a number, free to progress
        else:
            raise ValueError("invalid vector component passed: {0!r} is of type {1!r}".format(number,type(number)))
             
    def __init__(self, *args, **kwargs):
        """
        NOTE - components will always be returned in alphanumberic order. This can 
        result in confusing numbering for vectors with 10 or more components:
            a1, a10, a11, ..., a2, a21, ..., a3, a4, a5
        Components can be listed as individual arguments, passed in a single list
        or tuple, passed as a dictionary, or passed with component names. Component
        name 'name' is reserved for naming argument for components. By default
        2D and 3D vectors will use i, j, and k component vectors. Vectors in higher
        dimensions will be numbered 0, 1, 2... or n1, n2, n3... depending on if
        'name' is specified. Specifying name as '' will overide ijk formating but
        use numbers counting from 0 too. Passing named arguments afterwards can
        overide previous inputs; eg Vector(1,2,3, j=0) gives <1,0,3>. Since arguments
        can have custom names, user beware with how vector components interact in
        vector operations. Default behavior is positional-based, but strict component
        name checks can be used. <-- TODO
        """
        
        inputKeys = ['name']
        
        self.components = {}
        tempComponents = {}
        try:
            name = str(kwargs['name'])
            del kwargs['name']
        except:
            name = ''
        
        if ((len(args) + len(kwargs)) == 0):
            raise ValueError("cannot create a 0-dimensional (trivial) vector")
            
        if (len(args) != 0):
            # Can only use positional arguments if any are passed
            if (type(args[0]) == list or type(args[0]) == tuple):
                # Vector specified as a list or tuple (only first one given taken into conseration)
                comps = args[0]
                if ((len(comps) == 2 or len(comps) == 3) and name == ''):
                    # 2D or 3D vector in the list or tuple
                    # Name with unit vectors ijk
                    tempComponents = dict(zip(Vector.__unitComponents, map(Vector.__checkNum, comps)))
                else:
                    # Components are not 2D or 3D
                    # Name using 0, 1, 2... or 'n0', 'n1', 'n2'... depending on if passed a 'name' argument
                    for n in range(len(comps)):
                        tempName = name + str(n+1)
                        try:
                            tempName = int(tempName) - 1
                        except:
                            pass
                        tempComponents[tempName] = Vector.__checkNum(comps[n])
            
            elif (type(args[0]) == dict):
                # Vector specified as a dictionary maping
                comps = args[0]
                for key in comps:
                    tempComponents[key] = Vector.__checkNum(comps[key])
                
            elif ((len(args) == 2 or len(args) == 3) and name == ''):
                # 2D or 3D vector specified by elements without specific components
                # Name with unit vectors ijk
                tempComponents = dict(zip(Vector.__unitComponents, map(Vector.__checkNum, args)))
                
            else:
                # Components are not 2D or 3D
                # Name using 0, 1, 2... or 'n0', 'n1', 'n2'... depending on if passed a 'name' argument
                for n in range(len(args)):
                    tempName = name + str(n+1)
                    try:
                        tempName = int(tempName) - 1
                    except:
                        pass
                    tempComponents[tempName] = Vector.__checkNum(args[n])
                
        for key in kwargs:
            # Vector components specified by component name
            # Assign components excluding named function arguments
            if (key in inputKeys):
                continue
            tempComponents[key] = Vector.__checkNum(kwargs[key])
        
        self.__spaceSize = len(tempComponents)
        
        for key in sorted(tempComponents):
            # Alphabetize components for consistancy
            self.components[key] = tempComponents[key]
            
    def __repr__(self):
        # Overload text-based vector object representation
        string = '⟨'
        string = string + ', '.join(['{0!r}: {1}'.format(key,self.components[key]) for key in self.components])
        string = string + '⟩'
        return string
    
    def __str__(self):
        # Overload vector-to-string conversion. Basically above but without component names
        string = '⟨'
        string = string + ', '.join(['{0}'.format(self.components[key]) for key in self.components])
        string = string + '⟩'
        return string
    
    def __getitem__(self, key):
        # Overload indexing [] operation
        keyList = list(self.components.keys())
        if (key in keyList):
            return self.components[key]
        else:
            try:
                return self.components[keyList[key]]
            except IndexError:
                raise IndexError("vector component index is out of range")
            except:
                raise KeyError(key)
                
    def __setitem__(self, key, value):
        # Overload index-based assignment v[comp] = n
        if (type(value) != int and type(value) != float):
            raise TypeError("cannot assign a vector component to a non-scalar")
        keyList = list(self.components.keys())
        if (key in keyList):
            self.components[key] = value
        else:
            try:
                self.components[keyList[key]] = value
            except IndexError:
                raise IndexError("vector component index is out of range")
            except:
                raise KeyError(key)
    
    def __len__(self):
        # Overload length operation
        return self.__spaceSize
    
    def __iter__(self):
        # Overload iterator, useful for lists and tuples of components
        # No current workaround for dict(vect) returning component dictionary,
        # just use vect.components for now, but be careful with changing values
        for key in self.components:
            yield self.components[key]
    
    def __abs__(self):
        # Overload absolute value operation - i.e. magnatude
        retVal = 0
        for key in self.components:
            retVal += self.components[key] ** 2
        return math.sqrt(retVal)
    
    def __eq__(self, other):
        # Overload == comparison
        if (not isinstance(other, Vector)):
            return False
        if (self.__spaceSize != other.__spaceSize):
            return False
        for key1, key2 in zip(self.components.keys(), other.components.keys()):
            if (self.components[key1] != other.components[key2]):
                return False
        return True
        
    def __ne__(self, other):
        # Overload != comparison
        return not self.__eq__(other)
    
    def __neg__(self):
        # Overload negation '-'
        outVect = {}
        for key in self.components:
            outVect[key] = - self.components[key]
        return Vector(outVect)
    
    def __add__(self, other):
        # Overload addition operation
        # NOTE - keeps components of first vector passed
        if (type(other) != Vector):
            raise TypeError("cannot add a non-vector to a vector")
        if (self.__spaceSize != other.__spaceSize):
            raise ValueError("cannot add two vectors of different size")
        outVect = {}
        for key1, key2 in zip(self.components.keys(), other.components.keys()):
            outVect[key1] = self.components[key1] + other.components[key2]
        return Vector(outVect)
    
    def __iadd__(self, other):
        # Overload add-assign operator +=
        if (type(other) != Vector):
            raise TypeError("cannot add a non-vector to a vector")
        if (self.__spaceSize != other.__spaceSize):
            raise ValueError("cannot add two vectors of different size")
        for key1, key2 in zip(self.components.keys(), other.components.keys()):
            self.components[key1] += other.components[key2]
        return self
            
    def __sub__(self, other):
        # Overload addition operation
        # NOTE - keeps components of first vector passed
        if (type(other) != Vector):
            raise TypeError("cannot subtract a non-vector from a vector")
        if (self.__spaceSize != other.__spaceSize):
            raise ValueError("cannot subtract two vectors of different size")
        outVect = {}
        for key1, key2 in zip(self.components.keys(), other.components.keys()):
            outVect[key1] = self.components[key1] - other.components[key2]
        return Vector(outVect)
    
    def __isub__(self, other):
        # Overload subtract-assign operator -=
        if (type(other) != Vector):
            raise TypeError("cannot subtract a non-vector from a vector")
        if (self.__spaceSize != other.__spaceSize):
            raise ValueError("cannot subtract two vectors of different size")
        for key1, key2 in zip(self.components.keys(), other.components.keys()):
            self.components[key1] -= other.components[key2]
        return self
    
    def __mul__(self, other):
        # Overload multiplication operation
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot multiply a vector by a non-scalar")
        outVect = {}
        for key in self.components:
            outVect[key] = self.components[key] * other
        return Vector(outVect)
    
    def __rmul__(self, other):
        # Overload multiplication operation (reversed order x * Vector)
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot multiply a vector by a non-scalar")
        outVect = {}
        for key in self.components:
            outVect[key] = self.components[key] * other
        return Vector(outVect)
    
    def __imul__(self, other):
        # Overload multiply-assign operator *=
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot multiply a vector by a non-scalar")
        for key in self.components:
            self.components[key] *= other
        return self
    
    def __truediv__(self, other):
        # Overload division operation
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot divide a vector by a non-scalar")
        outVect = {}
        for key in self.components:
            outVect[key] = self.components[key] / other
        return Vector(outVect)
    
    def __idiv__(self, other):
        # Overload divide-assign operator /=
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot divide a vector by a non-scalar")
        for key in self.components:
            self.components[key] /= other
        return self
    
    def __floordiv__(self, other):
        # Overload floor-division operation
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot divide a vector by a non-scalar")
        outVect = {}
        for key in self.components:
            outVect[key] = self.components[key] // other
        return Vector(outVect)
    
    def __ifloordiv__(self, other):
        # Overload floor-divide-assign operator //=
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot divide a vector by a non-scalar")
        for key in self.components:
            self.components[key] //= other
        return self
    
    def __mod__(self, other):
        # Overload modulo operation
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot modulus a vector by a non-scalar")
        outVect = {}
        for key in self.components:
            outVect[key] = self.components[key] % other
        return Vector(outVect)
    
    def __imod__(self, other):
        # Overload modulo-assign operator %=
        if (type(other) != int and type(other) != float):
            raise TypeError("cannot modulus a vector by a non-scalar")
        for key in self.components:
            self.components[key] %= other
        return self