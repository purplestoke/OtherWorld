from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import hashlib
import base58
from Objects.BallotObjects import Ballot
import time

class Account:
    def __init__(self):
        self.pubKey = None
        self.privKey = None
        self.key = None
        self.addr = None
        self.nonce = 0
        self.transactions = {}
    
    def generate(self):
        key = RSA.generate(2048)
        self.key = key
        self.pub_key = self.getPubKey()
        self.priv_key = self.getPrivKey()
        self.addr = self.getAddress()
        self.transactions = {}
        self.nonce = 0

    def getPubKey(self):
        if self.key:
            return self.key.publickey().export_key()
        else:
            raise ValueError("Key not generated")

    def getPrivKey(self):
        if self.key:
            return self.key.export_key()
        else:
            raise ValueError("Key not generated")

    def getAddress(self):
        if not self.pub_key:
            raise ValueError("Public Key not generated")
        
        # HASH PUBLIC KEY 
        pubKeyHash = SHA256.new(self.pub_key).digest()

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

    def incrementNonce(self):
        self.nonce += 1

    def addTx(self, tx):
        self.transactions[self.nonce] = tx

    def generateVoteTransaction(self, ballot, vote):
        self.tx = self.VoteTransaction(self.pub_key, ballot, vote)
        self.tx.setupTx()

    def signTx(self):
            # SIGN OFF ON TRANSACTION
            signature = pkcs1_15.new(self.key).sign(self.tx.tx_hash)
            if self.verifyTx() == True:
                return signature
            else: return False
                 
    def verifyTx(self):
        try:
            pub_key_obj = RSA.import_key(self.pub_key)
            pkcs1_15.new(pub_key_obj).verify(self.tx.tx_hash, self.tx.signature)
            return True
        except (ValueError,TypeError): 
            return False


    # TRANSACTION CLASS NESTED WITHIN ACCOUNT CLASS
    """
    THIS CLASS IS NESTED WITHIN THE ACCOUNT CLASS SO THAT THE SIGNING OF 
    A TRANSACTIONS REMAINS INTERNAL. ie THE PRIVATE KEY STAYS WITHIN THE ACCOUNT.
    """
    class VoteTransaction:
        def __init__(self, public_key, ballot: Ballot, vote):
            self.public_key = public_key
            self.ballot = ballot
            self.vote = vote
            self.signature = None

        def setupTx(self):
            hash_str = f"{self.ballot.ballotHash}{self.vote}{self.account.nonce}{time.time()}".encode()
            self.tx_hash = SHA256.new(hash_str)

        
    """
    METHOD WHICH CREATES AN INSTANCE OF THE TRANSACTION CLASS
    INCREMENTS THE ACCOUNT NONCE AND SIGNS OFF ON THE NEWLY CREATED TRANSACTION
    """
    def createAndSignTx(self, ballot: Ballot, vote):
        # INCREMENT ACCOUNT NONCE SO TX INDEX IS CORRECT WITHIN ACCOUNT DICT
        self.incrementNonce()
        self.tx = self.VoteTransaction(self.pub_key, ballot, vote)
        self.tx.setupTx()
        signature = self.signTx(self.tx)
        if signature:
            self.transactions[self.nonce] = signature 
        

        