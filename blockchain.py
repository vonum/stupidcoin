import datetime
import hashlib
import json
from urllib.parse import urlparse
import requests

from block.block import Block, block_hash

class Blockchain:
  def __init__(self):
    self.chain = []
    self.mempool = []

    self.create_block(1, "0")

  def create_block(self, proof, previous_hash):
    block = Block(len(self.chain) + 1,
                  str(datetime.datetime.now()),
                  proof,
                  previous_hash,
                  self.mempool)
    self.mempool = []
    self.chain.append(block)

    return block

  def previous_block(self):
    return self.chain[-1]

  def proof_of_work(self, previous_proof):
    new_proof = 1
    check_proof = False

    while (not check_proof):
      hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

      if (hash_operation[:4] == "0000"):
        check_proof = True
      else:
        new_proof += 1

    return new_proof

  def is_chain_valid(self, chain):
    previous_block = chain[0]
    block_index = 1

    while (block_index < self.length()):
      block = self.chain[block_index]

      if not(self.is_block_valid(block, previous_block)):
        return False

      previous_block = block
      block_index += 1

    return True

  def is_block_valid(self, block, previous_block):
    if (block.previous_hash != block_hash(previous_block)):
      return False

    previous_proof = previous_block.proof
    proof = block.proof

    hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

    if (hash_operation[:4] != "0000"):
      return False

    return True

  def add_transaction(self, tx):
    self.mempool.append(tx)
    return tx

  def add_block(self, block):
    if self._contains_block(block):
      return False

    if self.is_block_valid(block, self.previous_block()):
      self.chain.append(block)
      self._remove_txs_from_mempool(block.transactions)
      return True
    else:
      return False

  def sync_chain(self):
    longest_chain = self.chain
    max_length = len(self.chain)

    for node in self.nodes:
      resp = requests.get(f"{node}/chain").json()
      chain = resp["chain"]
      length = resp["length"]

      if (self.is_chain_valid(chain) and length > len(longest_chain)):
        longest_chain = chain
        max_length = length

    self.chain = longest_chain

  def _contains_block(self, block):
    for b in self.chain:
      if b.blockhash == block.blockhash:
        return True

    return False

  def _remove_txs_from_mempool(self, txs):
    self.mempool = list(set(self.mempool) - set(txs))
