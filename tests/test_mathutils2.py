import pytest
from sympy import Poly, GF
from sympy.abc import x
from ntru.mathutils import is_prime, is_2_power, invert_poly

def test_is_prime():
    assert is_prime(7)
    assert not is_prime(9)

def test_is_2_power():
    assert is_2_power(8)
    assert not is_2_power(10)

def test_invert_poly_mod_prime():
    f = Poly(x + 1, x, domain=GF(3))
    R = Poly(x**2 + 1, x, domain=GF(3))
    g = invert_poly(f, R, 3)
    assert ((f * g) % R) == Poly(1, x, domain=GF(3))

