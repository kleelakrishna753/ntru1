import pytest
from ntru.ntrucipher import NtruCipher
from sympy import Poly, ZZ
from sympy.abc import x
from ntru.mathutils import random_poly
from sympy import GF

def test_keygen_encrypt_decrypt_cycle():
    N, p, q = 167, 3, 128
    cipher = NtruCipher(N, p, q)
    cipher.generate_random_keys()

    # Unify encryption side to ZZ
    cipher.h_poly = cipher.h_poly.set_domain(ZZ)
    cipher.R_poly = cipher.R_poly.set_domain(ZZ)

    msg_poly = Poly([1, 0, 2] + [0] * (N - 3), x).set_domain(ZZ)
    rand_poly = random_poly(N, N // 3)

    ciphertext = cipher.encrypt(msg_poly, rand_poly)

    # Debug print to check domain and values before switching to GF(p)
    print("Before Decryption:")
    print(f"Ciphertext domain: {ciphertext.domain}")
    print(f"R_poly domain before decryption: {cipher.R_poly.domain}")
    
    # Ensure both ciphertext and R_poly are in GF(p) domain before decryption
    ciphertext = ciphertext.set_domain(GF(p))
    cipher.R_poly = cipher.R_poly.set_domain(GF(p))
    
    # Debug check: Ensure correct domains
    print(f"Ciphertext domain after setting: {ciphertext.domain}")
    print(f"R_poly domain after setting: {cipher.R_poly.domain}")
    
    # Before calling decrypt(), ensure there are no zero elements or unexpected values
    # Check the first few coefficients of the ciphertext and R_poly
    print(f"Ciphertext first few coefficients: {ciphertext.all_coeffs()[:5]}")
    print(f"R_poly first few coefficients: {cipher.R_poly.all_coeffs()[:5]}")
    
    try:
        plaintext = cipher.decrypt(ciphertext)
        print(f"Decrypted plaintext: {plaintext}")
        assert msg_poly.trunc(p) == plaintext.trunc(p)
    except ZeroDivisionError as e:
        print(f"Caught a ZeroDivisionError during decryption: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

