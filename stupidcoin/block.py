from typing import List
from dataclasses import dataclass, field
from dataclasses import dataclass
from .transaction import Transaction
from .hashing import sha256

@dataclass
class Block:
  blockhash:     str = field(init=False)
  index:         int
  timestamp:     str
  proof:         int
  previous_hash: str
  transactions:  List[Transaction]

  def __post_init__(self):
    self.blockhash = block_hash(self)

  def to_string(self):
    return str(self)

  def to_payload(self):
    return {
      "index": self.index,
      "timestamp": self.timestamp,
      "proof": self.proof,
      "previous_hash": self.previous_hash,
      "transactions": [
        {"sender": tx.sender, "receiver": tx.receiver, "value": tx.value}
        for tx in self.transactions
      ]
    }

def block_hash(block):
  if block.index == 1:
    return "0"

  block_dict = {"index": block.index,
                "timestamp": block.timestamp,
                "proof": block.proof,
                "previous_hash": block.previous_hash,
                "tx": block.transactions}
  return sha256(str(block_dict))

def block_from_payload(payload):
  txs = [
    Transaction(tx["sender"], tx["receiver"], tx["value"])
    for tx in payload["transactions"]
  ]
  return Block(payload["index"],
               payload["timestamp"],
               payload["proof"],
               payload["previous_hash"],
               txs)
