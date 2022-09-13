import json
import datetime
import hashlib
import requests

from .block import Block, block_hash
from .constants import BLOCK_REWARD

class Blockchain:
  def __init__(self, initial_addresses):
    self.balances = {}
    for a in initial_addresses:
      self.balances[a] = 1000

    self.chain = []
    self.mempool = []

    self.create_block(1, "0", first=True)

  def create_block(self, proof, previous_hash, first=False):
    block = Block(len(self.chain) + 1,
                  str(datetime.datetime.now()),
                  proof,
                  previous_hash,
                  self.mempool)
    self.mempool = []

    if not(first):
      self._execute_block_transactions(block.transactions)
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

    while (block_index < len(self.chain)):
      block = self.chain[block_index]

      if not(self._is_block_valid(block, previous_block)):
        return False

      previous_block = block
      block_index += 1

    return True

  def add_transaction(self, tx, coinbase=False):
    if self._is_transaction_valid(tx, coinbase=coinbase):
      self.mempool.append(tx)

    return tx

  def add_block(self, block):
    if self._contains_block(block):
      return False

    if self._is_block_valid(block, self.previous_block()):
      self._execute_block_transactions(block.transactions)
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

  def _is_block_valid(self, block, previous_block):
    if (block.previous_hash != block_hash(previous_block)):
      return False

    previous_proof = previous_block.proof
    proof = block.proof

    hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

    if (hash_operation[:4] != "0000"):
      return False

    if not(self._are_block_transactions_valid(block.transactions)):
      return False

    return True

  def _contains_block(self, block):
    for b in self.chain:
      if b.blockhash == block.blockhash:
        return True

    return False

  def _remove_txs_from_mempool(self, txs):
    self.mempool = list(set(self.mempool) - set(txs))

  def _are_block_transactions_valid(self, txs):
    for tx in txs[:-1]:
      if not(self._is_transaction_valid(tx)):
        return False
    if not(self._is_transaction_valid(txs[-1], coinbase=True)):
      return False

    return True

  def _is_transaction_valid(self, tx, coinbase=False):
    if coinbase:
      if tx.value != BLOCK_REWARD:
        raise "Bad block reward"
    else:
      if self.balances[tx.sender] < tx.value:
        raise "Not enough coins"

    return True

  def _execute_block_transactions(self, txs):
    for tx in txs[:-1]:
      self._execute_transaction(tx)

    self._execute_transaction(txs[-1], coinbase=True)

  def _execute_transaction(self, tx, coinbase=False):
    if not(coinbase):
      self.balances[tx.sender] -= tx.value
    self.balances[tx.receiver] = self.balances.get(tx.receiver, 0) + tx.value
