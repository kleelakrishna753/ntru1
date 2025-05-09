import pytest
import numpy as np
from ntru.ntrucipher import NtruCipher
from sympy.abc import x
from sympy import Poly, ZZ
from ntru.mathutils import random_poly

def test_key_generation():
    ntru = NtruCipher(N=11, p=3, q=32)
    ntru.generate_random_keys()
    assert ntru.f_poly is not None
    assert ntru.h_poly is not None

def test_encrypt_decrypt_roundtrip():
    N, p, q = 11, 3, 32
    ntru = NtruCipher(N, p, q)
    ntru.generate_random_keys()

    message = Poly([1, 0, 1] + [0] * (N - 3), x).set_domain(ZZ)
    r = random_poly(N, 2)

    cipher = ntru.encrypt(message, r)
    decrypted = ntru.decrypt(cipher)

    assert message == decrypted, "Roundtrip encryption-decryption failed"

