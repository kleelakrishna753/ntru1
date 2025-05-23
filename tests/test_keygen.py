import numpy as np
import os
from ntru.ntrucipher import NtruCipher

def test_key_generation():
    N, p, q = 11, 3, 32
    cipher = NtruCipher(N, p, q)
    cipher.generate_random_keys()

    assert cipher.h_poly is not None
    assert cipher.f_poly is not None
    assert cipher.f_p_poly is not None

    # Test encryption and decryption
    original_message = "hi"
    ciphertext = cipher.encrypt(original_message)
    decrypted_message = cipher.decrypt(ciphertext)

    # Validate encryption-decryption cycle
    assert decrypted_message == original_message, \
        f"Decrypted message '{decrypted_message}' does not match original '{original_message}'"

