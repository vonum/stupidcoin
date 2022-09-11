from typing import List
from fastapi import FastAPI, Body
from uuid import uuid4
from blockchain import Blockchain
from block.wallet import Wallet
from block.transaction import Transaction

node_address = str(uuid4()).replace("-", "")

app = FastAPI()
app.blockchain = Blockchain()
app.wallet = Wallet.generate(None)

@app.get("/chain")
async def chain():
  return {"length": app.blockchain.length(), "chain": app.blockchain.chain}

@app.get("/mempool")
async def mempool():
  return {"length": app.blockchain.mempool_length(), "chain": app.blockchain.mempool}

@app.get("/is_valid")
async def is_valid():
  chain = app.blockchain.chain
  return {"valid": app.blockchain.is_chain_valid(chain)}

@app.get("/latest_block")
async def latest_block():
  return app.blockchain.chain[-1]

@app.get("/mine_block")
async def mine_block():
  previous_block = app.blockchain.previous_block()
  previous_hash = app.blockchain.hash(previous_block)

  coinbase_tx = Transaction(node_address, "milan", 1)
  app.blockchain.add_transaction(coinbase_tx)

  proof = app.blockchain.proof_of_work(previous_block.proof)
  block = app.blockchain.create_block(proof, previous_hash)

  return block

@app.post("/add_transaction")
async def add_transaction(sender: str = Body(...),
                          receiver: str = Body(...),
                          value: int = Body(...),
                          signature: str = Body(...),
                          public_key: str = Body(...)):
  tx = Transaction(sender, receiver, value)

  for t in app.blockchain.mempool:
    if tx.txhash == t.txhash:
      return tx

  message = tx.to_string()

  # If tx not in mempool, add it and forward it to connected nodes
  if (Wallet.verify(message, signature, public_key)):
    app.blockchain.add_transaction(tx)
    forward_tx(app.wallet, tx, signature, public_key, app.blockchain.nodes)
    return tx
  else:
    raise "Invalid signature"

@app.post("/add_nodes")
async def add_nodes(node_urls: List = Body(..., embed=True)):
  app.blockchain.add_nodes(node_urls)
  return app.blockchain.nodes

@app.post("/sync_chain")
async def sync_chain():
  app.blockchain.sync_chain()
  return app.blockchain.chain

def forward_tx(wallet, tx, signature, public_key, nodes):
  for node in nodes:
    try:
      wallet.forward_transaction(tx, signature, public_key, node)
    except:
      print(f"Failed to forward tx to {node}")
