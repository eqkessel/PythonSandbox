
from enum import Enum
import numbers as num
import numpy as np

class _axis_modes(Enum):
    CARTESIAN   = 0
    POLAR       = 1
    SPHERICAL   = 2

Cartesian   = _axis_modes.CARTESIAN
Polar       = _axis_modes.POLAR
Cylindrical = _axis_modes.POLAR
Spherical   = _axis_modes.SPHERICAL

#   Base Vector class
class BaseVector(np.ndarray):

    #   Member variable to track instance
    #__instance = None

    #   Validate value to set (unneeded, numpy already has validation)
    # def __validate(self, value):
    #     if (not isinstance(value, num.Number)):
    #         #   Raise exception if the value passed in is not PEP 3141 numerical, pass through otherwise
    #         raise ValueError("Invalid value passed; {0} is not numerical.".format(value))
    #     return value

    #   Instantiator function for BaseVector
    def __new__(cls, *args, **kwargs):
        #   Call __new__ for numpy ndarray, passing through arguments
        #return super(BaseVector,cls).__new__(cls, *args, **kwargs)
        #   Prevent the user from instantiating a BaseVector class
        raise NotImplementedError("Instantiating vectors from the BaseVector class is prohibited.")
    
    #   Getters-Setters for vector components
    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, value):
        self[0] = value #self.__validate(value)

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, value):
        self[1] = value #self.__validate(value)

    @property
    def r(self):
        return np.sqrt(self.x **2 + self.y **2)

    @r.setter
    def r(self, value):
        if (self.r == 0):
            raise ValueError("Unable to resize r component from zero")
        scale_factor = value / self.r
        self.x *= scale_factor
        self.y *= scale_factor
        # return self

    @property
    def theta(self):
        return np.arctan2(self.y, self.x)

    @theta.setter
    def theta(self, value):
        radius = self.r
        self.x = radius * np.cos(value)
        self.y = radius * np.sin(value)
        # return self

    @property
    def norm(self):
        length = abs(self)
        if (length == 0):
            raise ValueError("Cannot normalize a zero vector")
        return self / abs(self)

    #   Function overloads
    def __str__(self):
        # Overload vector-to-string conversion. Scalable to any size vector
        #string = '⟨'
        string = '<'
        string = string + ', '.join([str(value) for value in self])
        #string = string + '⟩'
        string = string + '>'
        return string

    def __abs__(self):
        #   Overload absolute value, interpret as vector magnatude
        #temp = np.array(self)
        return np.sqrt(np.sum(np.array(self, dtype=self.dtype)**2))

    #   Overload math operations to match vector math rules
    def __add__(self, other):
        #   Overload sum operation (+) to throw exception if not added to vector of same type
        vecType = type(self)
        if (not isinstance(other, vecType)):
            raise TypeError(f"Vector addition requires two vectors of same type: {type(other)}")
        return vecType(np.array(self, dtype=self.dtype) + np.array(other, dtype=self.dtype), dtype=self.dtype)

    def __radd__(self, other):
        #   Above but backwards (other + self)
        return self + other

    def __iadd__(self, other):
        #   Above but using in-place add (self += other)
        self = self + other
        return self

    def __sub__(self, other):
        #   Overload difference operation (-) to throw exception if not subtracted by vector of same type
        vecType = type(self)
        if (not isinstance(other, vecType)):
            raise TypeError(f"Vector subtraction requires two vectors of same type: {type(other)}")
        return vecType(np.array(self, dtype=self.dtype) - np.array(other, dtype=self.dtype), dtype=self.dtype)

    def __rsub__(self, other):
        #   Above but backwards (other - self)
        vecType = type(self)
        if (not isinstance(other, vecType)):
            raise TypeError(f"Vector subtraction requires two vectors of same type: {type(other)}")
        return vecType(np.array(other, dtype=self.dtype) - np.array(self, dtype=self.dtype), dtype=self.dtype)

    def __isub__(self, other):
        #   Above but using in-place subtract (self -= other)
        self = self - other
        return self

    def __mul__(self, other):
        #   Overload multiply to include dotting w/ another vector
        vecType = type(self)
        if (isinstance(other, vecType)):
            #   Two vectors, use dot product
            return np.sum(np.array(self, dtype=self.dtype) * np.array(other, dtype=self.dtype))
        elif (isinstance(other, num.Number)):
            #   Vector and scalar number, use scalar multiplication
            return vecType(np.array(self, dtype=self.dtype) * other, dtype=self.dtype)
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector multiplication: {type(other)}")

    def __rmul__(self, other):
        #   Overload reverse multiply (other * vector)
        #   Don't have to handle dot product in this case, just scalar check
        vecType = type(self)
        if (isinstance(other, num.Number)):
            return vecType(np.array(self, dtype=self.dtype) * other, dtype=self.dtype)
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector multiplication: {type(other)}")

    def __imul__(self, other):
        #   Overload in-place multiply *=, accept only scalars
        vecType = type(self)
        if (isinstance(other, num.Number)):
            self = vecType(np.array(self, dtype=self.dtype) * other, dtype=self.dtype)
            return self
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector multiplication: {type(other)}")

    def __truediv__(self, other):
        #   Overload divide (vec / other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            return vecType(np.array(self, dtype=self.dtype) / other, dtype=self.dtype)
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __itruediv__(self, other):
        #   Overload in-place divide (vec /= other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            self = vecType(np.array(self, dtype=self.dtype) / other, dtype=self.dtype)
            return self
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __floordiv__(self, other):
        #   Overload floor divide (vec // other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            return vecType(np.array(self, dtype=self.dtype) // other, dtype=self.dtype)
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __ifloordiv__(self, other):
        #   Overload in-place floor divide (vec //= other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            self = vecType(np.array(self, dtype=self.dtype) // other, dtype=self.dtype)
            return self
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __mod__(self, other):
        #   Overload modulo (vec % other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            return vecType(np.array(self, dtype=self.dtype) % other, dtype=self.dtype)
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __imod__(self, other):
        #   Overload in-place modulo (vec %= other) to throw excpetion if not passed a scalar
        vecType = type(self)
        if (isinstance(other, num.Number)):
            self = vecType(np.array(self, dtype=self.dtype) % other, dtype=self.dtype)
            return self
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __divmod__(self, other):
        #   Overload divmod(vec, other) to throw excpetion if not passed a scalar for other
        vecType = type(self)
        if (isinstance(other, num.Number)):
            return (vecType(np.array(self, dtype=self.dtype) // other, dtype=self.dtype),\
                    vecType(np.array(self, dtype=self.dtype) % other, dtype=self.dtype))
        #   Throw an exception for all other cases
        raise TypeError(f"Invalid type for vector division: {type(other)}")

    def __pow__(self, other):
        #   Overload power operation
        #   Check that exponenet is nonzero nonnegative integer
        if (int(other) == abs(other)):
            #   Power of vector alternates between scalar (on even powers) and vector (on odd powers)
            #   Start with value of 1 and repeatedly multiply/dot with vector
            result = 1
            for i in range(other):
                result = result * self
            return result
        else:
            raise ValueError(f"Cannot raise a vector to a negative or non-integer exponent: {other}")

    #   Overload illegal vector operations to throw exeptions
    def __rtruediv__(self, other):
        raise NotImplementedError("Cannot divide by a vector.")
    
    def __rfloordiv__(self, other):
        raise NotImplementedError("Cannot divide by a vector.")
    
    def __rmod__(self, other):
        raise NotImplementedError("Cannot divide by a vector.")
    
    def __rdivmod__(self, other):
        raise NotImplementedError("Cannot divide by a vector.")
    
    def __rpow__(self, other):
        raise NotImplementedError("Cannot raise to the power of a vector.")


#   2D Vector class
class Vector2(BaseVector):
    #   Instantiate a Vector2
    def __new__(cls, *args, mode = _axis_modes.CARTESIAN, **kwargs):
        #   Create a new empty 2x1 ndarray and pass through keyword arguments
        #print(super(Vector2, cls))
        instance = super(BaseVector, cls).__new__(cls, (2), **kwargs)

        instance.__call__(*args, mode = mode)
        # if (len(args) == 0):
        #     #   No parameters specified, create a zero vector
        #     instance.x = 0
        #     instance.y = 0
        # elif (len(args) == 1):
        #     #   Try as if first passed argument is array-like
        #     instance.x = args[0][0]
        #     instance.y = args[0][1]
        # elif (len(args) == 2):
        #     #   Two parameters passed, set as vector components
        #     instance.x = args[0]
        #     instance.y = args[1]

        return instance

    # #   Element getters and setters
    # @property
    # def x(self):
    #     return self[0]

    # @x.setter
    # def x(self, value):
    #     self[0] = value

    # @property
    # def y(self):
    #     return self[1]

    # @y.setter
    # def y(self, value):
    #     self[1] = value
    
    #   Overload call functionality to allow simultaneous modification of all elements
    def __call__(self, *args, mode = _axis_modes.CARTESIAN):
        if(not isinstance(mode, _axis_modes)):
            raise ValueError(f"Invalid vector coodinate conversion type passed: {mode}")

        nArgs = len(args)
        if (nArgs == 1):
            if (isinstance(args[0], complex)):
                #   Convert a single complex number to a 2D vector
                X = args[0].real
                Y = args[0].imag
            elif (isinstance(args[0], num.Real)):
                if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                    #   Create vector of the parameter's length along the x-axis
                    X = args[0]
                    Y = 0
                else:
                    #   Set all elements of vector to the same real number
                    X = args[0]
                    Y = args[0]
            elif (isinstance(args[0], BaseVector)):
                #   Copy vector, first 2 elements only
                X = args[0].x
                Y = args[0].y
            elif (len(args[0]) == 2 or len(args[0] == 3)):
                #   Argument is array-like with length of 2 or 3 (ignore 3rd coodinate)
                if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                    #   Parameter elements are in the form (r, theta)
                    X = args[0][0] * np.cos(args[0][1])
                    Y = args[0][0] * np.sin(args[0][1])
                else:
                    #   Parameter elements are in the form (x, y)
                    X = args[0][0]
                    Y = args[0][1]
        elif (nArgs == 2):
            #   Two parameters passed, treat as individual coordinates
            if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                #   Parameter elements are in the form (r, theta)
                X = args[0] * np.cos(args[1])
                Y = args[0] * np.sin(args[1])
            else:
                #   Parameter elements are in the form (x, y)
                X = args[0]
                Y = args[1]
        elif (nArgs == 0):
            #   No parameters specified, create a zero vector
            X = 0
            Y = 0
        else:
            #   Invalid parameters cast
            raise TypeError(f"Unable to coerce arguments passed to a 3D vector. Arguments passed:\n{args}")

        self.x = X
        self.y = Y

    #   Function overloads
    def __matmul__(self, other):
        #   Overload matrix multiply operator @ to function as 2D cross product
        if (not isinstance(other, type(self))):
            raise TypeError("Cross product of Vector2 requires another Vector2")
        return (self.x * other.y) - (self.y * other.x)

#   3D Vector class
class Vector3(BaseVector):
    #   Instantiate a Vector3
    def __new__(cls, *args, mode = _axis_modes.CARTESIAN, **kwargs):
        #   Create a new empty 2x1 ndarray and pass through keyword arguments
        #print(super(Vector2, cls))
        instance = super(BaseVector, cls).__new__(cls, (3), **kwargs)

        instance.__call__(*args, mode = mode)

        return instance

    #   Additional Element getters and setters
    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, value):
        self[2] = value

    @property
    def rho(self):
        return abs(self)

    @rho.setter
    def rho(self, value):
        self = self.norm * value

    @property
    def phi(self):
        return np.arctan2(self.r, self.z)

    @phi.setter
    def phi(self, value):
        rho = self.rho
        self.r = rho * np.sin(value)
        self.z = rho * np.cos(value)

    #   Overload call functionality to allow simultaneous modification of all elements
    def __call__(self, *args, mode = _axis_modes.CARTESIAN):
        if(not isinstance(mode, _axis_modes)):
            raise ValueError(f"Invalid vector coodinate conversion type passed: {mode}")

        nArgs = len(args)
        if (nArgs == 1):
            if (isinstance(args[0], complex)):
                #   Convert a single complex number to a 3D vector on xy plane (z=0)
                X = args[0].real
                Y = args[0].imag
                Z = 0
            elif (isinstance(args[0], num.Real)):
                if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                    #   Create vector of the parameter's length along the x-axis
                    X = args[0]
                    Y = 0
                    Z = 0
                else:
                    #   Set all elements of vector to the same real number
                    X = args[0]
                    Y = args[0]
                    Z = args[0]
            elif (isinstance(args[0], BaseVector)):
                #   Copy vector components
                X = args[0].x
                Y = args[0].y
                if (isinstance(args[0], type(self))):
                    #   Vector 3 Passed in, can copy Z-component
                    Z = args[0].z
                else:
                    #   2D vector in 3D space
                    Z = 0
            elif (len(args[0]) == 2):
                #   Argument is array-like with length of 2, treat as 3D vector on xy plane (z=0)
                if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                    #   Parameter elements are in the form (r, theta)
                    X = args[0][0] * np.cos(args[0][1])
                    Y = args[0][0] * np.sin(args[0][1])
                else:
                    #   Parameter elements are in the form (x, y)
                    X = args[0][0]
                    Y = args[0][1]
                Z = 0
            elif (len(args[0] == 3)):
                #   Argument is array-like with length 3
                if (mode == _axis_modes.POLAR):
                    #   Parameter elements are in the form (r, theta, z)
                    X = args[0][0] * np.cos(args[0][1])
                    Y = args[0][0] * np.sin(args[0][1])
                    Z = args[0][2]
                if (mode == _axis_modes.SPHERICAL):
                    #   Parameter elements are in the form (rho, theta, phi)
                    X = args[0][0] * np.cos(args[0][1]) * np.sin(args[0][2])
                    Y = args[0][0] * np.sin(args[0][1]) * np.sin(args[0][2])
                    Z = args[0][0] * np.cos(args[0][2])
                else:
                    #   Parameter elements are in the form (x, y, z)
                    X = args[0][0]
                    Y = args[0][1]
                    Z = args[0][2]
        elif (nArgs == 2):
            #   Two parameters passed, treat as individual coordinates for a 3D vector on xy plane (z=0)
            if (mode == _axis_modes.POLAR or mode == _axis_modes.SPHERICAL):
                #   Parameter elements are in the form (r, theta)
                X = args[0] * np.cos(args[1])
                Y = args[0] * np.sin(args[1])
            else:
                #   Parameter elements are in the form (x, y)
                X = args[0]
                Y = args[1]
            Z = 0
        elif (nArgs == 3):
            #   Three paramaters passed, treat as individual coordinates
            if (mode == _axis_modes.POLAR):
                #   Parameter elements are in the form (r, theta, z)
                X = args[0] * np.cos(args[1])
                Y = args[0] * np.sin(args[1])
                Z = args[2]
            elif (mode == _axis_modes.SPHERICAL):
                #   Parameter elements are in the form (rho, theta, phi)
                X = args[0] * np.cos(args[1]) * np.sin(args[2])
                Y = args[0] * np.sin(args[1]) * np.sin(args[2])
                Z = args[0] * np.cos(args[2])
            else:
                #   Parameter elements are in the form (x, y, z)
                X = args[0]
                Y = args[1]
                Z = args[2]
        elif (nArgs == 0):
            #   No parameters specified, create a zero vector
            X = 0
            Y = 0
            Z = 0
        else:
            #   Invalid parameters cast
            raise TypeError(f"Unable to coerce arguments passed to a 3D vector. Arguments passed:\n{args}")

        self.x = X
        self.y = Y
        self.z = Z

    #   Function overloads
    def __matmul__(self, other):
        #   Overload matrix multiply operator @ to function as 3D cross product
        if (not isinstance(other, type(self))):
            raise TypeError("Cross product of Vector3 requires another Vector3")

        # The easiest way to understand cross products is with the determinant of a matrix
        # with their components:
        #         | x^  y^  z^ |
        # a x b = | ax  ay  az | = <(ay*bz - az*by), (ax*bz - az*bx), (ax*by - ay*bx)>
        #         | bx  by  bz |

        X = (self.y * other.z) - (self.z * other.y)
        Y = (self.x * other.z) - (self.z * other.x)
        Z = (self.x * other.y) - (self.y * other.x)

        return Vector3(X, Y, Z, dtype=self.dtype)



        
"""
class Thing(np.ndarray):
    def __new__(cls, *args, **kwargs):
        print("Class is {0}, repr is {0!r}, type is {1}".format(cls,type(cls)))
        instance = super(Thing,cls).__new__(cls, (3), **kwargs)
        instance[0] = args[0]
        instance[1] = args[1]
        instance[2] = args[2]
        return instance
"""