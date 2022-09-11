import argparse

from block.wallet import Wallet
from block.constants import KEYS_DIRECTORY
from block.transaction import Transaction

parser = argparse.ArgumentParser()
parser.add_argument("--sender", "-s", type=int, help="[0, 9]")
parser.add_argument("--receiver", "-r", type=int, help="[0, 9]")
parser.add_argument("--value", "-v", type=int, help="> 0")
parser.add_argument("--port", "-p", type=int, help="")

args = parser.parse_args()

sender   = args.sender
receiver = args.receiver
value    = args.value
port     = args.port

with open(f"{KEYS_DIRECTORY}/{sender}.pkey", "r") as f:
  pkey = f.read()
  sender_wallet = Wallet.import_hex(pkey, port)

with open(f"{KEYS_DIRECTORY}/{receiver}.pkey", "r") as f:
  pkey = f.read()
  receiver_wallet = Wallet.import_hex(pkey, port)

tx = Transaction(sender_wallet.public_key(),
                 receiver_wallet.public_key(),
                 value)

r = sender_wallet.send_transaction(receiver_wallet.public_key(), 500)
print(r)
"""
message = tx.to_string()
signature = sender_wallet.sign(message)

print("Message: ", message)
print("Signature:", signature)
print("Public key:", sender_wallet.public_key())

status = Wallet.verify(message, signature, sender_wallet.public_key())
print(status)

data = {"sender": sender_wallet.public_key(),
        "receiver": receiver_wallet.public_key(),
        "value": value,
        "signature": signature,
        "public_key": sender_wallet.public_key()}

print(url)
r = requests.post(f"{url}/add_transaction", json=data)
print(r)
"""
