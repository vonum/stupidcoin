from dataclasses import dataclass, field
from .hashing import sha256

@dataclass
class Transaction:
  txhash:   str = field(init=False)
  sender:   str
  receiver: str
  value:    int

  def __post_init__(self):
    self.txhash = sha256(self.to_string())

  def to_string(self):
    tx_dict = {"sender": self.sender, "receiver": self.receiver, "value": self.value}
    return str(tx_dict)
