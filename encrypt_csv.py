import csv
import subprocess
import os

# Paths
csv_file = 'FN.csv'
output_dir = 'encrypted_chunks'
os.makedirs(output_dir, exist_ok=True)

with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Skip header

    for idx, row in enumerate(reader):
        row_str = ','.join(row).strip()

        if len(row_str) >= 40:
            print(f"⚠️ Skipping row {idx+1} (too long for NTRU): {row_str[:50]}...")
            continue

        plaintext_file = f'temp_row_{idx}.txt'
        encrypted_file = os.path.join(output_dir, f'encrypted_row_{idx}.bin')

        # Save row to temp file
        with open(plaintext_file, 'w') as f:
            f.write(row_str)

        # Run encryption
        with open(encrypted_file, 'wb') as outfile:
            result = subprocess.run(
                ['./ntru.py', 'enc', 'pub.key.npz', plaintext_file],
                stdout=outfile,
                stderr=subprocess.PIPE
            )

        # Check for errors
        if result.returncode != 0 or b"Input is too large" in result.stderr:
            print(f"❌ Error encrypting row {idx+1}: {result.stderr.decode().strip()}")
            os.remove(encrypted_file)
        else:
            print(f"✅ Encrypted row {idx+1} -> {encrypted_file}")

        # Clean up temp
        os.remove(plaintext_file)

