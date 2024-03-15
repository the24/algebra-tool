from typing import Tuple
from polynomial import Polynomial

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
