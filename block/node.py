import requests

from blockchain import Blockchain
from block.transaction import Transaction
from block.wallet import Wallet

class Node:
  def __init__(self):
    self.blockchain = Blockchain()
    self.wallet = Wallet.generate(None)
    self.nodes = set()

  def add_nodes(self, node_urls):
    self.nodes = self.nodes.union(node_urls)
    return self.nodes

  def chain_length(self):
    return self.blockchain.length()

  def chain(self):
    return self.blockchain.chain

  def mempool_length(self):
    return self.blockchain.mempool_length()

  def mempool(self):
    return self.blockchain.mempool

  def sync_chain(self):
    longest_chain = self.chain()
    max_length = len(longest_chain)

    for node in self.nodes:
      resp = requests.get(f"{node}/chain").json()
      chain = resp["chain"]
      length = resp["length"]

      if (self.is_chain_valid(chain) and length > len(longest_chain)):
        longest_chain = chain
        max_length = length

    self.blockchain.chain = longest_chain

  def is_chain_valid(self, chain):
    return self.blockchain.is_chain_valid(chain)

  def latest_block(self):
    return self.blockchain.previous_block()

  def mine_block(self):
    previous_block = self.blockchain.previous_block()
    previous_hash = self.blockchain.hash(previous_block)

    coinbase_tx = Transaction(self.wallet.public_key(), "milan", 1)
    self.blockchain.add_transaction(coinbase_tx)

    proof = self.blockchain.proof_of_work(previous_block.proof)
    block = self.blockchain.create_block(proof, previous_hash)

    return block

  def add_transaction(self, sender, receiver,
                      value, signature, public_key):
    tx = Transaction(sender, receiver, value)

    for t in self.mempool():
      if tx.txhash == t.txhash:
        return tx

    message = tx.to_string()

    # If tx not in mempool, add it and forward it to connected nodes
    if (Wallet.verify(message, signature, public_key)):
      self.blockchain.add_transaction(tx)
      self._forward_tx(tx, signature, public_key)
      return tx
    else:
      raise "Invalid signature"

  def _forward_block(self, block):
    for node in self.nodes:
      try:
        pass
      except:
        print(f"Failed to forward block to {node}")

  def _forward_tx(self, tx, signature, public_key):
    for node in self.nodes:
      try:
        self.wallet.forward_transaction(tx, signature, public_key, node)
      except:
        print(f"Failed to forward tx to {node}")
