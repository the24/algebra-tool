from typing import List, Union, Self
from numbers import Rational, RationalLike

class Polynomial:
    """
    Representation of a polynomial by a list of coefficient.
    Where P[n] is the coefficient of X^n.
    All the coefficient of the polinomial is a rational.

    Example :
    X^4 + 3X^2 + -2X + 1
    => [1, -2, 3, 0, 1]

    Attributes:
        coef: the list of coefficient of the polinomial
    """

    def __init__(self, coef: RationalLike):        
        self.coef = list(map(Rational.to_rational, coef))
    
    def __len__(self):
        return len(self.coef)

    def __getitem__(self, index: int):
        return self.coef[index]
    
    def __setitem__(self, index: int, x: RationalLike):
        self.coef[index] = Rational.to_rational(x)
    
    def __str__(self):
        s = ""

        for i in range(len(self)):
            if i == 0:
                s += "{:>6}".format(self[i])
            elif i == 1:
                s += "{:>6}X".format(self[i])
            else:
                s += "{:>6}X^{}".format(self[i], i)
            if i != len(self)-1: s += " + "
        
        return s

    def __add__(self, other):
        deg = max(len(self), len(other))

        S = Polynomial([0]*deg)

        for i in range(deg):
            if i >= len(self):
                S[i] = other[i]
            elif i >= len(other):
                S[i] = self[i]
            else:
                S[i] = self[i] + other[i]
        
        S.clean()

        return S
    
    def __mul__(self, other):
        if isinstance(other, (int, Rational)):
            other = Polynomial([other])
        
        lenM = len(self)+len(other)-1
        M = Polynomial([0]*(lenM))
        
        for i in range(lenM):
            Mk = 0
            for k in range(i+1):
                # TODO: optimize the loop to avoid checking
                if k >= len(self) or i-k >= len(other):
                    continue
                Mk += self[k]*other[i-k]
            
            M[i] = Mk

        return M
    
    def __truediv__(self, other):
        if isinstance(other, (int, Rational)):
            return self*(Rational(1,1)/other)
    
    def __rmul__(self, other):
        return self * other
    
    def clean(self):
        """
        Remove leading 0 of the polynomial, so the lenght of coef still
        correspond to degree+1.
        """
        # TODO: Use a while loop ??
        for i in range(len(self)-1, 0, -1):
            if self[i] == 0:
                self.coef.pop()
            else:
                break
    
    def __eq__(self, other):
        if isinstance(other, int):
            other = Polynomial([other])

        if len(self) != len(other):
            return False
        
        for i in range(len(self)):
            if self.coef[i] != other.coef[i]:
                return False
        
        return True

    def __ne__(self, other):
        return not self == other
