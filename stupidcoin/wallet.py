import requests
from ecdsa import SigningKey, VerifyingKey

from .constants import node_url
from .hashing import sha256_bytes
from .transaction import Transaction

class Wallet:
  def __init__(self, pkey, port):
    self.pkey = pkey
    self.node_url = node_url(port)

  @classmethod
  def import_hex(cls, hex_pkey, port):
    bytes_pkey = bytes.fromhex(hex_pkey)
    pkey = SigningKey.from_string(bytes_pkey)
    return Wallet(pkey, port)

  @classmethod
  def generate(cls, port):
    pkey = SigningKey.generate()
    return Wallet(pkey, port)

  @classmethod
  def verify(cls, message, signature, key):
    bytes_signature = bytes.fromhex(signature)
    bytes_message = sha256_bytes(message)
    bytes_key = bytes.fromhex(key)
    pubkey = VerifyingKey.from_string(bytes_key)
    return pubkey.verify(bytes_signature, bytes_message)

  def sign(self, message):
    bytes_message = sha256_bytes(message)
    return self.pkey.sign(bytes_message).hex()

  def private_key(self):
    return self.pkey.to_string().hex()

  def public_key(self):
    pubkey = self.pkey.verifying_key
    return pubkey.to_string().hex()

  def send_transaction(self, receiver, value):
    tx = Transaction(self.public_key(), receiver, value)
    message = tx.to_string()
    signature = self.sign(message)

    payload = self._transaction_payload(tx, signature)
    return self._post_transaction(payload)

  def _transaction_payload(self, tx, signature):
    return {"sender":     tx.sender,
            "receiver":   tx.receiver,
            "value":      tx.value,
            "signature":  signature,
            "public_key": self.public_key()}

  def _post_transaction(self, payload):
    return requests.post(f"{self.node_url}/add_transaction", json=payload)
