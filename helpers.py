import hashlib

# Buffer size for hash calculation.
BUF_SIZE = 65536

# Calculate SHA256 hash for a file.
# https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
def calculate_sha256(file):
    try:
        sha256 = hashlib.sha256()

        with open(file, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    except:
        return None
