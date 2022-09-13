# stupidcoin
Very simple and stupid simulation of a blockchain.
There are no background processes, so everything needs to be triggered manually
(minning).
When blocks are mined, all transactions from the mempool are taken.
No support for orphan blocks.

## Setup
1. `git clone git@github.com:vonum/stupidcoin.git`
2. `pip install -r requirements.txt`
3. `python generate_key_pairs.py`

This will generate 10 key pairs for testing purposes which are placed in `keys`
directory.

## Simulating the blockchain
Each address in the `keys` directory will have an initial balance of 1000 coins.

### Starting the nodes
1. `uvicorn app:app --reload --port PORT`
2. `curl -X POST -H 'Content-type: application/json' --data '{"node_urls": ["OTHER_NODE_URL"]}' NODE_URL/add_nodes`

### Sending transactions
Only transactions supported are transfering tokens.
To send transactions, pass the following parameters:

1. SENDER_ID -> id of sender wallet (ie 0) [0, 9]
2. RECEIVER_ID -> id of receiver wallet (ie 3) [0, 9]
3. VALUE -> number of coins to transfer
4. PORT -> port of node you wish to target

`python send_tx.py -s SENDER_ID -r RECEIVER_ID -v VALUE -p PORT`

Transactions will be forwarded to all connected nodes and they will forward them
further.

### Minning blocks
All transactions from the mempool will be added to the block.

`curl NODE_URL/mine_block`

Block will be forwarded to all connected nodes and they forward them further.

### Getting info from node
1. `curl NODE_URL/chain`
2. `curl NODE_URL/mempool`
3. `curl NODE_URL/balances`
