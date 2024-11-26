from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import hashlib
import base58
from Objects.BallotObjects import Ballot   
import time

class Account:
    def __init__(self):
        self.__pub_key = None
        self.__key = None
        self.addr = None
        self.__nonce = 0
        self.__transactions = {}
    
    # FILLS IN CLASS VAR FIELDS
    def generate(self):
        self.__key = RSA.generate(2048)
        self.__pub_key = self.__key.publickey().export_key()
        self.addr = self.createAddress()

    def getPubKey(self):
        return self.__pub_key

    def createAddress(self):
        if not self.__pub_key:
            raise ValueError("Public Key not generated")
        return self.encodeAddress(self.__pub_key)
    
    def encodeAddress(self, publicKey):
        # HASH PUBLIC KEY 
        pubKeyHash = SHA256.new(publicKey).digest()

        # RIPEMD-160 ON PUBKEY HASH
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(pubKeyHash)
        ripemd160Hash = ripemd160.digest()

        # ADD NETWORK BYTE
        netByte = b'\x00'
        extendedKey = netByte + ripemd160Hash

        # CREATE CHECKSUM 
        checksum = SHA256.new(SHA256.new(extendedKey).digest()).digest()[:4]

        # ADD CHECKSUM TO extendedKey
        finalKey = extendedKey + checksum

        # ENCODE RESULT WITH BASE58 TO GET ADDRESS
        address = base58.b58encode(finalKey)

        return address.decode('utf-8')

    def getNonce(self):
        return self.__nonce
    
    def getTransactions(self):
        return self.__transactions

    def incrementNonce(self):
        self.__nonce += 1

    def decrementNonce(self):
        self.__nonce -= 1

    def addTx(self, tx):
        self.__transactions[self.__nonce] = tx

    def signTx(self, tx_hash):
            # SIGN OFF ON TRANSACTION
            signature = pkcs1_15.new(self.__key).sign(tx_hash)
            if self.verifyTx(tx_hash, signature):
                return signature
            else: 
                return False
                 
    def verifyTx(self, tx_hash, signature):
        try:
            pub_key_obj = RSA.import_key(self.getPubKey())
            pkcs1_15.new(pub_key_obj).verify(tx_hash, signature)
            return True
        except (ValueError,TypeError): 
            return False

    # TRANSACTION CLASS NESTED WITHIN ACCOUNT CLASS
    """
    THIS CLASS IS NESTED WITHIN THE ACCOUNT CLASS SO THAT THE SIGNING OF 
    A TRANSACTIONS REMAINS INTERNAL. ie THE PRIVATE KEY STAYS WITHIN THE ACCOUNT.
    """
    class VoteTransaction:
        def __init__(self, nonce, ballot: Ballot, vote):
            self.nonce = nonce
            self.ballot = ballot
            self.vote = vote

        def setupTx(self):
            hash_str = f"{self.ballot.getBallotHash()}{self.vote}{self.nonce}{time.time()}".encode()
            self.tx_hash = SHA256.new(hash_str)
            return self.tx_hash.digest() != b''
    
    def createVoteTransactionObject(self, ballot, vote):
        return self.VoteTransaction(self.__nonce, ballot, vote)
   
    """
    METHOD WHICH CREATES AN INSTANCE OF THE TRANSACTION CLASS
    INCREMENTS THE ACCOUNT NONCE AND SIGNS OFF ON THE NEWLY CREATED TRANSACTION
    """
    def createAndSignTx(self, ballot, vote):
        self.incrementNonce()
        # CREATE VOTE TX OBJ
        vote_transaction_object = self.createVoteTransactionObject(ballot, vote)
        if vote_transaction_object.setupTx():
            signature = self.signTx(vote_transaction_object.tx_hash)
            if signature:
                self.addTx(signature)
                return True
        else:
            self.decrementNonce()
            return False 
        

        