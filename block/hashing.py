import hashlib

def sha256_bytes(message):
  hashed_message = sha256(message)
  return bytes.fromhex(hashed_message)

def sha256(message):
  return hashlib.sha256(message.encode()).hexdigest()
