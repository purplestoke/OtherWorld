import hashlib
import time 

"""
EACH BLOCK WILL BE ADDED TO THE BLOCKCHAIN CLASS
A BLOCK CONTAINS ACCOUNT SIGNATURES WHICH SIGNED OFF ON BALLOTS
"""

class Block:
    def __init__(self, index, previous_hash, data, timestamp, nonce=0):
        self.__index = index
        self.__previous_hash = previous_hash
        self.__data = data
        self.__timestamp = timestamp
        self.__nonce = nonce
        self.__hash = self.computeHash()

    def computeHash(self):
        blockStr = f"{self.__index}{self.__previous_hash}{self.__data}{self.__timestamp}{self.__nonce}".encode()
        return hashlib.sha256(blockStr).hexdigest()
    
    def getBlockHash(self):
        return self.__hash
    
    def getBlockPreviousHash(self):
        return self.__previous_hash
    
    def getBlockTimestamp(self):
        return self.__timestamp
    
    def getBlockIndex(self):
        return self.__index
    
    def getBlockNonce(self):
        return self.__nonce
    
    def getBlockData(self):
        return self.__data

    def setBlockNonce(self, new_nonce):
        self.__nonce = new_nonce

    def setBlockHash(self, new_hash):
        self.__hash = new_hash

    def getContents(self):
        hsh = self.getBlockHash()
        prev_hsh = self.getBlockPreviousHash()
        timestmp = self.getBlockTimestamp()
        nonce = self.getBlockNonce()
        data = self.getBlockData()
        block_dict = {"Block Hash": hsh, "Previous Block Hash": prev_hsh, "Nonce": nonce, "Data": data, "Timestamp": timestmp}
        return block_dict
class Blockchain:
    def __init__(self):
        self.__chain = []
        self.__diff = 4
        self.createGenesisBlock()

    def getBlockByIndex(self, i):
        return self.__chain[i]

    def getLatestBlock(self):
        return self.__chain[-1]
    
    def addBlock(self, block: Block): 
        block.computeHash()
        self.__chain.append(block)

    def proofOfWork(self, block: Block):
        block.setBlockNonce(0)
        i = 0
        while not block.getBlockHash().startswith('0' * self.__diff):
            i += 1
            block.setBlockNonce(i)
            new_hash = block.computeHash()
            block.setBlockHash(new_hash)
        return block.getBlockHash() 

    def getChain(self):
        return self.__chain
    
    # FIRST BLOCK CREATED
    # DOES NOT HOLD ANY VOTE INFORMATION
    def createGenesisBlock(self):
        blk = Block(0, '0', "Genesis Block", time.time())
        self.__chain.append(blk)