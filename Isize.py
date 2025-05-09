import csv
import numpy as np

# Path to your CSV file
csv_path = 'FN.csv'

# Read and concatenate all cell values as a single string
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header if needed
    combined_text = ""

    for row in reader:
        combined_text += ''.join(row)  # Concatenate without separators

# Encode to bytes and print the size
byte_data = combined_text.encode('utf-8')
print(f"Total character count: {len(combined_text)}")
print(f"Total byte size for encryption: {len(byte_data)} bytes")

with open(csv_path, "rb") as f:
    raw = f.read()
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    print("Total bits:", len(bits))

