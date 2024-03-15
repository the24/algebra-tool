from math import gcd
from typing import List, Union, Self

class Rational:
    """
    Quotient of two integers.

    Attributes:
        p: numerator
        q: denominator
    """

    def __init__(self, p: int, q: int):
        # TODO: accept float and convert it to Rational
        if (not isinstance(p, int) or not isinstance(q, int)):
            raise TypeError("numerator and denominator must be interger")
        self.p = p
        self.q = q
    
    def __str__(self):
        if self.q == 1:
            return "{}".format(self.p)
        elif self.p == 0:
            return "0"
        else:
            return "{}/{}".format(self.p, self.q)

    def __repr__(self):
        if self.q == 1:
            return "{}".format(self.p)
        elif self.p == 0:
            return "0"
        else:
            return "{}/{}".format(self.p, self.q)
    
    def __format__(self, spec):
        if spec.startswith(">"):
            val = int(spec[1:]) - len(str(self))
            return " "*val + str(self)
        elif spec.startswith("<"):
            val = int(spec[1:]) - len(str(self))
            return str(self) + " "*val
        else:
            pass
    
    def simplify(self):
        """
        Makes numerator and denominator relatively prime and denominator
        positive.
        """

        d = gcd(self.p, self.q)
        self.p = self.p // d
        self.q = self.q // d

        if (self.q < 0):
            self.q *= -1
            self.p *= -1
        
        return self
    
    def __add__(self, other):
        s = Rational(0, 0)
        if isinstance(other, Rational):
            s.p = (self.p * other.q + other.p * self.q)
            s.q = self.q * other.q
        elif isinstance(other, int):
            s.p = (self.p + other*self.q)
            s.q = self.q
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'" \
                                .format(type(self), type(other)))
        return s.simplify()
    
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        other = -other
        return self+other
    
    def __neg__(self):
        return Rational(-self.p, self.q)

    def __mul__(self, other):
        # TODO: Accept float
        if isinstance(other, Rational):
            return Rational(self.p*other.p, self.q*other.q)
        elif isinstance(other, int):
            return Rational(self.p*other, self.q)
        else:
            try:
                return other * self
            except TypeError:
                raise
    
    def __truediv__(self, other):
        # TODO: Accept float
        if isinstance(other, int):
            return Rational(self.p, self.q*other)
        elif isinstance(other, Rational):
            return Rational(self.p * other.q, self.q * other.p)
        else:
            raise TypeError()
    
    def __eq__(self, other):
        if isinstance(other, Rational):
            return self.p * other.q == self.q * other.p
        elif isinstance(other, int):
            return self.p == self.q * other
    
    def __ne__(self, other):
        return not self == other
    
    @classmethod
    def to_rational(cls, x: Union[Self, int]) -> Self:
        if isinstance(x, Rational):
            return x
        elif isinstance(x, int):
                return Rational(x, 1)
        else:
            raise TypeError("can not convert {} to Rational".format({type(x)}))

RationalLike = Union[List[int], List[Rational]]
