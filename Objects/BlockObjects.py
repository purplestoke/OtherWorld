import hashlib
import time 

class Block:
    def __init__(self, index, prevHash, data, timestamp, nonce=0):
        self.index = index
        self.prevHash = prevHash
        self.data = data
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.computeHash()

    def computeHash(self):
        blockStr = f"{self.index}{self.prevHash}{self.data}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(blockStr).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.diff = 4
        self.createGenesisBlock()

    def getLatestBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        block.prevHash = self.getLatestBlock().hash
        block.hash = block.computeHash()
        self.chain.append(block)

    def proofOfWork(self, block):
        block.nonce = 0
        while not block.hash.startswith('0' * self.diff):
            block.nonce += 1
            block.hash = block.computeHash()
        return block.hash 

    def createGenesisBlock(self):
        blk = Block(0, '0', "Genesis Block", time.time())
        self.chain.append(blk)

