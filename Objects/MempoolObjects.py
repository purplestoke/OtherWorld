from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from queue import LifoQueue
from pymerkle import InmemoryTree as MerkleTree


class Mempool:
    def __init__(self):
        self.__pool = LifoQueue()

    def addTransaction(self, tx):
        self.__pool.put(tx)

    # REMOVES MOST RECENTLY ADDED TX
    def removeTransaction(self):
        if not self.__pool.empty():
            tx = self.__pool.get()
            return tx
        else: return None

    def getTxs(self):
        transactions = list(self.__pool.queue)
        return transactions
    
    def getTxAtIndex(self, i):
        transactions = self.getTxs()
        if transactions:
            if 0 <= i < len(transactions):
                return transactions[i]
            else: return None



