from math import gcd
from typing import List, Tuple, Union, Self


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


class GCDPolynomialCalculator:
    """
    Matrix used to calculate gcd and Bezout coefficient of two polynomial with
    Blankinship algorithm.

    The matrix is represented as :
        x1  x2  P
        y1  y2  Q
    and initialized as :
        1   0   P
        0   1   Q
    """

    def __init__(self, P: Polynomial, Q: Polynomial):
        self.x1 = Polynomial([1])
        self.x2 = Polynomial([0])
        self.y1 = Polynomial([0])
        self.y2 = Polynomial([1])
        self.P  = P
        self.Q  = Q
    
    def __str__(self):
        # TODO: Clean code
        sx1 = str(self.x1)
        sx2 = str(self.x2)
        sy1 = str(self.y1)
        sy2 = str(self.y2)
        sP = str(self.P)
        sQ = str(self.Q)
        
        # Align two lines
        diff1 = len(sx1) - len(sy1)
        diff2 = len(sx2) - len(sy2)
        diff3 = len(sP)  - len(sQ)

        L1 = ""
        L1 +=  sx1 + " "*min(0, -diff1) + " | "
        L1 +=  sx2 + " "*min(0, -diff2) + " | "
        L1 +=  sP  + " "*min(0, -diff3)

        L2 = ""
        L2 += sy1 + " "*max(0, diff1) + " | "
        L2 += sy2 + " "*max(0, diff2) + " | "
        L2 += sQ  + " "*max(0, diff3)
        return L1+"\n"+L2
    
    def switch(self):
        """
        Inverts the two lines
        """
        self.x1, self.y1 = self.y1, self.x1
        self.x2, self.y2 = self.y2, self.x2
        self.P,  self.Q  = self.Q,  self.P
    
    def next_step(self):
        degP = len(self.P)-1
        degQ = len(self.Q)-1
        diff = degP - degQ

        if diff < 0:
            self.switch()
            degP, degQ = degQ, degP
            diff *= -1
        
        coef = -self.P[degP]/self.Q[degQ]
        R = coef*Polynomial([0]*diff + [1])
        self.P += self.Q*R
        self.x1 += self.y1*R
        self.x2 += self.y2*R
    
    def solve(self, print_step=False) -> Tuple[Polynomial, Polynomial, Polynomial]:
        """
        Compute the gcd and bezout coefficient with Blankinship algorithm.

        Args:
            print_step: show all step leading to result
        
        Returns:
            A tuple containing in order the bezout coefficient of P, the
            coefficient of Q and the gcd of P and Q.
        """
        
        while self.P != 0 and self.Q != 0:
            self.next_step()
            if print_step: print(self, "\n")
        
        if self.P == 0:
            main_coef = self.Q[len(self.Q)-1]
            return (self.y1/main_coef, self.y2/main_coef, self.Q/main_coef)
        elif self.Q == 0:
            main_coef = self.P[len(self.P)-1]
            return (self.x1/main_coef, self.x2/main_coef, self.P/main_coef)


if __name__ == "__main__":
    # P = X^4 + X^3 - 3X^2 - 4X - 1
    P = Polynomial([-1, -4, 3, 1, 1])

    # Q = X^3 + X^2 - X - 1
    Q = Polynomial([-1, -1, 1, 1])

    print("P   = ", P)
    print("Q   = ", Q)
    print("")

    (U, V, GCD) = GCDPolynomialCalculator(P, Q).solve()

    print("U   = ", U)
    print("V   = ", V)
    print("GCD = ", GCD)
    print(P*U + Q*V == GCD)