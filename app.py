from typing import List
from fastapi import FastAPI, Body
from uuid import uuid4
from block.node import Node

app = FastAPI()
app.node = Node()

@app.get("/chain")
async def chain():
  return {"length": app.node.chain_length(), "chain": app.node.chain()}

@app.get("/mempool")
async def mempool():
  return {"length": app.node.mempool_length(), "mempool": app.node.mempool()}

@app.get("/is_valid")
async def is_valid():
  chain = app.node.chain()
  return {"valid": app.node.is_chain_valid(chain)}

@app.get("/latest_block")
async def latest_block():
  return app.node.latest_block()

@app.get("/mine_block")
async def mine_block():
  return app.node.mine_block()

@app.post("/add_transaction")
async def add_transaction(sender: str = Body(...),
                          receiver: str = Body(...),
                          value: int = Body(...),
                          signature: str = Body(...),
                          public_key: str = Body(...)):
  app.node.add_transaction(sender, receiver, value,
                           signature, public_key)
@app.post("/add_nodes")
async def add_nodes(node_urls: List = Body(..., embed=True)):
  app.node.add_nodes(node_urls)
  return app.node.nodes

@app.post("/sync_chain")
async def sync_chain():
  app.node.sync_chain()
  return app.node.chain()
