import argparse
import numpy as np
import math
from sympy import symbols, Poly, ZZ
from ntru.ntrucipher import NtruCipher
from ntru.mathutils import random_poly
import sys

x = symbols('x')

def text_to_bits(data):
    return ''.join(f'{byte:08b}' for byte in data)

def bits_to_bytes(bitstr):
    pad_len = (8 - len(bitstr) % 8) % 8
    bitstr += '0' * pad_len
    return int(bitstr, 2).to_bytes(len(bitstr) // 8, byteorder='big')

def encrypt_file(pubkey_path, input_path, output_path):
    pub = np.load(pubkey_path, allow_pickle=True)
    N = int(pub['N']); p = int(pub['p']); q = int(pub['q'])
    cipher = NtruCipher(N, p, q)
    cipher.h_poly = Poly(list(pub['h'][::-1]), x).set_domain(ZZ)

    with open(input_path, 'rb') as f:
        data = f.read()
    bitstr = text_to_bits(data)
    pad_len = (-len(bitstr)) % N
    bitstr += '0' * pad_len

    encrypted_bits = ''
    for i in range(0, len(bitstr), N):
        block = bitstr[i:i+N]
        coeffs = [int(b) for b in block]
        m_poly = Poly(sum(int(coeffs[j]) * x**j for j in range(N)), x).set_domain(ZZ)
        r_poly = random_poly(N, int(math.sqrt(q)))
        c_poly = cipher.encrypt(m_poly, r_poly)
        c_coeffs = [int(c_poly.coeff_monomial(x**j)) for j in range(N)]
        encrypted_bits += ''.join(f'{c:013b}' for c in c_coeffs)

    with open(output_path, 'wb') as f:
        f.write(bits_to_bytes(encrypted_bits))

def decrypt_file(privkey_path, input_path, output_path):
    priv = np.load(privkey_path, allow_pickle=True)
    N = int(priv['N']); p = int(priv['p']); q = int(priv['q'])
    cipher = NtruCipher(N, p, q)
    cipher.f_poly = Poly(list(priv['f'][::-1]), x).set_domain(ZZ)
    cipher.f_p_poly = Poly(list(priv['f_p'][::-1]), x).set_domain(ZZ)

    with open(input_path, 'rb') as f:
        data = f.read()
    bitstr = ''.join(f'{byte:08b}' for byte in data)
    block_len = N * 13
    bitstr = bitstr[:len(bitstr) - len(bitstr) % block_len]

    msg_bits = ''
    for i in range(0, len(bitstr), block_len):
        block = bitstr[i:i+block_len]
        c_coeffs = [int(block[j*13:(j+1)*13], 2) for j in range(N)]
        c_poly = Poly(sum(int(c_coeffs[j]) * x**j for j in range(N)), x).set_domain(ZZ)
        m_poly = cipher.decrypt(c_poly)
        m_coeffs = [int(m_poly.coeff_monomial(x**j)) for j in range(N)]
        msg_bits += ''.join(str(c) for c in m_coeffs)

    msg_bits = msg_bits[:len(msg_bits) - len(msg_bits) % 8]
    with open(output_path, 'wb') as f:
        f.write(bits_to_bytes(msg_bits))

def main():
    parser = argparse.ArgumentParser(description="NTRU Encrypt/Decrypt CSV")
    subparsers = parser.add_subparsers(dest='command', required=True)

    enc = subparsers.add_parser('encrypt')
    enc.add_argument('--pubkey', required=True)
    enc.add_argument('--input', required=True)
    enc.add_argument('--output', required=True)

    dec = subparsers.add_parser('decrypt')
    dec.add_argument('--privkey', required=True)
    dec.add_argument('--input', required=True)
    dec.add_argument('--output', required=True)

    args = parser.parse_args()

    if args.command == 'encrypt':
        encrypt_file(args.pubkey, args.input, args.output)
    elif args.command == 'decrypt':
        decrypt_file(args.privkey, args.input, args.output)
    else:
        print("Invalid command")
        sys.exit(1)

if __name__ == '__main__':
    main()

