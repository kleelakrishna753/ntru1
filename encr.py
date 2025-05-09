import csv
import subprocess
import os

# Paths
csv_file = 'FN.csv'
encrypted_file = 'encrypted_chunks/encrypted_data.bin'  # Specify the full path
os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)  # Ensure directory exists

with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header

    encrypted_data = bytearray()  # To hold all the encrypted rows as a byte array

    for idx, row in enumerate(reader):
        row_str = ','.join(row).strip()

        if len(row_str) >= 40:
            print(f"⚠️ Skipping row {idx+1} (too long for NTRU): {row_str[:50]}...")
            continue

        plaintext_file = f'temp_row_{idx}.txt'

        # Save row to temp file
        with open(plaintext_file, 'w') as f:
            f.write(row_str)

        # Run encryption
        result = subprocess.run(
            ['./ntru.py', 'enc', 'pub.key.npz', plaintext_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Check for errors
        if result.returncode != 0 or b"Input is too large" in result.stderr:
            print(f"❌ Error encrypting row {idx+1}: {result.stderr.decode().strip()}")
        else:
            print(f"✅ Encrypted row {idx+1}")

            # Append the encrypted data to the bytearray
            encrypted_data.extend(result.stdout)

        # Clean up temp plaintext file
        os.remove(plaintext_file)

    # Save all encrypted data to a single file
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)

print(f"✅ All rows encrypted and saved to {encrypted_file}")

