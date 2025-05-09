import numpy as np
import os
from ntru.ntrucipher import NtruCipher

def test_key_generation():
    N, p, q = 167, 3, 4096
    cipher = NtruCipher(N, p, q)
    cipher.generate_random_keys()

    assert cipher.h_poly is not None
    assert cipher.f_poly is not None
    assert cipher.f_p_poly is not None

