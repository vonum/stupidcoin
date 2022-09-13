KEYS_DIRECTORY = "keys"
NODE_BASE_URL = "http://localhost"
BLOCK_REWARD = 100

def node_url(port):
  return f"{NODE_BASE_URL}:{port}"
