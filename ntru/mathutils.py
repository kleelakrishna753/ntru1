import math
from sympy import GF, invert
import logging
import numpy as np
from sympy.abc import x
from sympy import ZZ, Poly

log = logging.getLogger("mathutils")


def is_prime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_2_power(n):
    return n != 0 and (n & (n - 1) == 0)


def random_poly(length, d, neg_ones_diff=0):
    return Poly(np.random.permutation(
        np.concatenate((np.zeros(length - 2 * d - neg_ones_diff), np.ones(d), -np.ones(d + neg_ones_diff)))),
        x).set_domain(ZZ)


from sympy.polys.domains import ZZ as sympyZZ

def invert_poly(f_poly, R_poly, p):
    if is_prime(p):
        f_poly = f_poly.set_domain(GF(p))
        R_poly = R_poly.set_domain(GF(p))
        return invert(f_poly, R_poly, domain=GF(p))

    elif is_2_power(p):
        # Start with inverse mod 2
        f_mod2 = f_poly.set_domain(GF(2))
        R_mod2 = R_poly.set_domain(GF(2))
        g = invert(f_mod2, R_mod2, domain=GF(2))

        # Lift inverse using Newton–Raphson
        g = g.set_domain(ZZ)
        f_poly = f_poly.set_domain(ZZ)
        R_poly = R_poly.set_domain(ZZ)

        k = 2
        while k < p:
            g = ((2 * g - f_poly * g**2) % R_poly).trunc(k)
            k *= 2
        return g.trunc(p).set_domain(GF(p))  # ← This is the key fix

    else:
        raise Exception(f"Cannot invert polynomial modulo Z_{p}")




