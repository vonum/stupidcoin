import argparse

from stupidcoin.wallet import Wallet
from stupidcoin.constants import KEYS_DIRECTORY
from stupidcoin.transaction import Transaction

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

r = sender_wallet.send_transaction(receiver_wallet.public_key(), value)
print(f"Sent {value} from {sender_wallet.public_key()} to {receiver_wallet.public_key()}")
