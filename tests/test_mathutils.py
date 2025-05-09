from ntru.mathutils import random_poly
import numpy as np

def test_random_poly_range():
    poly = random_poly(10, 3)
    assert all(-3 <= c <= 3 for c in poly.all_coeffs())

