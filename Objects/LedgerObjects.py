from pymerkle import InmemoryTree as MerkleTree
import pickle

"""
READS THE BLOCKCHAIN STATE AND ORGANIZES THE INFORMATION IN A JSON FORMAT
MUST HAVE A CONCISE SET OF RULES FOR CREATING ITSELF
"""

class Ledger:
    def __init__(self):
        self.txList = []
        self.merkleTree = MerkleTree(algorithm='sha256')
        self.rootHash = None
    
    def addTx(self, tx):
        self.merkleTree.append_entry(tx)
        self.rootHash = self.merkleTree.get_state()

    
