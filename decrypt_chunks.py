import os
import subprocess

encrypted_dir = 'encrypted_chunks'
decrypted_dir = 'decrypted_rows'
os.makedirs(decrypted_dir, exist_ok=True)

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

