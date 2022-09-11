from typing import List
from dataclasses import dataclass
from .transaction import Transaction

@dataclass
class Block:
  index: int
  timestamp: int
  proof: str
  previous_hash: str
  transactions: List[Transaction]

  def to_string(self):
    return str(self)
