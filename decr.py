import os
import csv
import subprocess
import numpy as np

# Paths
encrypted_file = 'encrypted_chunks/encrypted_data.bin'  # Single encrypted file with all rows
decrypted_file = 'decrypted_rows/decrypted_rows.csv'  # Output file to save decrypted rows
priv_key_file = 'priv.key.npz'  # Private key file

# Function to decrypt a single chunk (row)
def decrypt(priv_key_file, encrypted_chunk):
    result = subprocess.run(
        ['./ntru.py', 'dec', priv_key_file],
        input=encrypted_chunk,  # Pass the chunk of encrypted data as input
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print(f"❌ Error decrypting chunk: {result.stderr.decode().strip()}")
        return None

    # Return the decrypted text (assuming it's in a comma-separated format)
    return result.stdout.decode().strip()

# Function to read the encrypted file, decrypt each row, and save to CSV
def decrypt_and_save(encrypted_file, decrypted_file, priv_key_file):
    with open(encrypted_file, 'rb') as f:
        encrypted_data = f.read()

    # Assuming each encrypted row is of a fixed size (you must adjust this value)
    row_size = 1024  # Adjust to match the actual encrypted row size
    total_rows = len(encrypted_data) // row_size

    decrypted_rows = []
    for i in range(total_rows):
        # Extract the encrypted data for the current row
        start = i * row_size
        end = (i + 1) * row_size
        encrypted_row = encrypted_data[start:end]

        # Decrypt the row
        decrypted_row = decrypt(priv_key_file, encrypted_row)
        if decrypted_row:
            decrypted_rows.append(decrypted_row)

    # Write the decrypted rows to a CSV file
    with open(decrypted_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in decrypted_rows:
            # Split each decrypted row by commas (since it was originally CSV formatted)
            writer.writerow(row.split(','))

    print(f"✅ Decrypted rows saved to {decrypted_file}")

# Run the decryption and saving process
decrypt_and_save(encrypted_file, decrypted_file, priv_key_file)

