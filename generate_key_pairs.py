from block.wallet import Wallet
from block.constants import KEYS_DIRECTORY

for i in range(10):
  print(i)

  w = Wallet.generate()
  pkey = w.private_key()

  with open(f"{KEYS_DIRECTORY}/{i}.pkey", "w") as f:
    f.write(pkey)


w1 = Wallet.generate()
w2 = Wallet.generate()

p1 = w1.private_key()
p2 = w2.private_key()

w3 = Wallet.import_hex(p1)
w4 = Wallet.import_hex(p2)

print(w3.private_key())
print(w4.private_key())
