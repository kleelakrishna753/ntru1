import numpy as np
import os
from ntru.ntrucipher import NtruCipher
from ntru.mathutils import generate_random_small_poly

def test_key_generation():
    N, p, q = 11, 3, 32  # Use small values for easier debugging
    cipher = NtruCipher(N, p, q)
    cipher.generate_random_keys()

    assert cipher.h_poly is not None
    assert cipher.f_poly is not None
    assert cipher.f_p_poly is not None

    # Test encryption and decryption
    original_message = "hi"

    # Generate a random small polynomial for encryption
    rand_poly = generate_random_small_poly(N, num_ones=5, num_neg_ones=5)

    ciphertext = cipher.encrypt(original_message, rand_poly)
    decrypted_message = cipher.decrypt(ciphertext)

    assert decrypted_message == original_message, \
        f"Decrypted message '{decrypted_message}' does not match original '{original_message}'"

