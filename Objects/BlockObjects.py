import hashlib
import time 
from Objects.LedgerObjects import Ledger

class Block:
    def __init__(self, index, previous_hash, transactions: Ledger, timestamp):
        self.header = self.Header(self.computeHash(), index, timestamp, previous_hash)
        self.transactions = transactions
    

    def computeHash(self):
        block_str = f"{self.header.index}{self.header.previous_hash}{self.transactions.rootHash}{self.header.timestamp}{self.header.nonce}".encode()
        return hashlib.sha256(block_str).hexdigest()

    # HOLDS BASIC INFORMATION ABOUT THE BLOCK
    class Header:
        def __init__(self, block_hash, index, timestamp, previous_hash):
            self.block_hash = block_hash
            self.index = index 
            self.timestamp = timestamp
            self.previous_hash = previous_hash
            self.nonce = None

  
class Blockchain:
    def __init__(self):
        self.chain = []
        self.diff = 4
        self.createGenesisBlock()

    def getLatestBlock(self):
        return self.chain[-1]

    def addBlock(self, block: Block):
        block.previous_hash = self.getLatestBlock().hash
        block.hash = block.computeHash()
        self.chain.append(block)

    def proofOfWork(self, block: Block):
        block.nonce = 0
        while not block.hash.startswith('0' * self.diff):
            block.nonce += 1
            block.hash = block.computeHash()
        return block.hash 

    def createGenesisBlock(self):
        blk = Block(0, '0', "Genesis Block", time.time())
        self.chain.append(blk)

    def getBlockByIndex(self, index):
        return self.chain[index]