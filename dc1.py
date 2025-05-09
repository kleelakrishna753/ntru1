import os
import subprocess
import csv

# Directories
encrypted_dir = 'encrypted_chunks'
decrypted_dir = 'decrypted_rows'
output_csv = 'dc1o.csv'

# Create directories if they don't exist
os.makedirs(decrypted_dir, exist_ok=True)

# Open the CSV file for writing (write mode, header included)
with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Process each encrypted file
    for filename in sorted(os.listdir(encrypted_dir)):
        if filename.endswith('.bin'):
            encrypted_path = os.path.join(encrypted_dir, filename)
            decrypted_path = os.path.join(decrypted_dir, filename.replace('.bin', '.txt'))

            with open(decrypted_path, 'w') as outfile:
                result = subprocess.run(
                    ['./ntru.py', 'dec', 'priv.key.npz', encrypted_path],
                    stdout=outfile,
                    stderr=subprocess.PIPE
                )

            if result.returncode != 0:
                print(f"❌ Failed to decrypt {filename}: {result.stderr.decode().strip()}")
                os.remove(decrypted_path)
            else:
                print(f"✅ Decrypted {filename} -> {decrypted_path}")

                # After decryption, read the decrypted text and write to CSV
                with open(decrypted_path, 'r') as decrypted_file:
                    # Assuming each decrypted file has one line/row
                    decrypted_content = decrypted_file.read().strip()
                    
                    # Split the content into fields (adjust according to your data format)
                    # For example, splitting by spaces or any delimiter
                    row = decrypted_content.split()  # Adjust the split logic if needed

                    # Append the decrypted row to the CSV
                    csv_writer.writerow(row)

print(f"✅ All decrypted rows have been saved to {output_csv}")

