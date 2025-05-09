import numpy as np
from ntru.ntrucipher import NtruCipher
from sympy.abc import x
from sympy import ZZ, Poly
from ntru.mathutils import random_poly

def test_encrypt_decrypt():
    N, p, q = 11, 3, 32
    ntru = NtruCipher(N, p, q)
    ntru.generate_random_keys()

    msg = np.random.randint(0, p, size=N)
    r = random_poly(N, 2)

    ciphertext = ntru.encrypt(Poly(msg[::-1], x).set_domain(ZZ), r)
    plaintext = ntru.decrypt(ciphertext).all_coeffs()[::-1]

    # Trim and compare
    plaintext = np.array(plaintext[-len(msg):], dtype=int) % p
    assert np.array_equal(msg % p, plaintext)

