from typing import List, Dict
from fastapi import FastAPI, Body, Request
from uuid import uuid4

from stupidcoin.constants import KEYS_DIRECTORY
from stupidcoin.node import Node
from stupidcoin.wallet import Wallet
from stupidcoin.block import block_from_payload

import os

initial_addresses = []
for filename in os.listdir(KEYS_DIRECTORY):
    if filename == ".keep":
      continue
    filepath = os.path.join(KEYS_DIRECTORY, filename)

    with open(filepath, "r") as f:
      pkey = f.read()
      wallet = Wallet.import_hex(pkey, None)
      initial_addresses.append(wallet.public_key())
print(initial_addresses)

app = FastAPI()
app.node = Node(initial_addresses)

@app.get("/chain")
async def chain():
  return {"length": app.node.chain_length(), "chain": app.node.chain()}

@app.get("/mempool")
async def mempool():
  return {"length": app.node.mempool_length(), "mempool": app.node.mempool()}

@app.get("/balances")
async def chain():
  return app.node.blockchain.balances

@app.get("/is_valid")
async def is_valid():
  chain = app.node.chain()
  return {"valid": app.node.is_chain_valid(chain)}

@app.get("/latest_block")
async def latest_block():
  return app.node.latest_block()

@app.get("/mine_block")
async def mine_block():
  block = app.node.mine_block()
  app.node.forward_block(block)
  return block

@app.post("/add_block")
async def add_block(index: int = Body(...),
                    timestamp: str = Body(...),
                    proof: int = Body(...),
                    previous_hash: str = Body(...),
                    transactions: List[Dict] = Body(...)):
  block = block_from_payload({
    "index": index,
    "timestamp": timestamp,
    "proof": proof,
    "previous_hash": previous_hash,
    "transactions": transactions
  })
  if (app.node.add_block(block)):
    app.node.forward_block(block)

@app.post("/add_transaction")
async def add_transaction(sender: str = Body(...),
                          receiver: str = Body(...),
                          value: int = Body(...),
                          signature: str = Body(...),
                          public_key: str = Body(...)):
  tx = app.node.add_transaction(sender, receiver, value,
                           signature, public_key)
@app.post("/add_nodes")
async def add_nodes(node_urls: List = Body(..., embed=True)):
  app.node.add_nodes(node_urls)
  return app.node.nodes

@app.post("/sync_chain")
async def sync_chain():
  app.node.sync_chain()
  return app.node.chain()
