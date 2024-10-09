from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import hashlib
import base58

class Account:
    def __init__(self):
        self.pubKey = None
        self.privKey = None
        self.key = None
        self.addr = None
        self.nonce = 0
        self.transactions = []
    
    # GENERATE A KEY PAIR
    # CALLS getPubKey() AND getPrivKey() METHODS
    def generate(self):
        key = RSA.generate(2048)
        self.key = key
        self.pubKey = self.getPubKey()
        self.privKey = self.getPrivKey()
        self.addr = self.getAddress()

    # PULL PUBLIC KEY FROM self.key INTERNAL VAR
    def getPubKey(self):
        if self.key:
            return self.key.publickey().export_key()
        else:
            raise ValueError("Key not generated")

    # PULL PRIVATE KEY FROM self.key INTERNAL VAR
    def getPrivKey(self):
        if self.key:
            return self.key.export_key()
        else:
            raise ValueError("Key not generated")

    # GENERATE AN ADDRESS FROM PUBLIC KEY
    def getAddress(self):
        if not self.pubKey:
            raise ValueError("Public Key not generated")
        
        # HASH PUBLIC KEY 
        pubKeyHash = SHA256.new(self.pubKey).digest()

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

    # SIGN A BALLOT WITH ACCOUNT PRIVATE KEY 
    def signBallot(self, ballotHash, ballotIdentifier, ballotName, ballotData, ballotAuthor):
        if ballotHash.digest() == SHA256.new(f"{ballotIdentifier}{ballotName}{ballotData}{ballotAuthor}".encode()).digest():
            sig = pkcs1_15.new(self.key).sign(ballotHash)

        # VERIFY SIGNATURE
        try:
            pubKeyObj = RSA.import_key(self.pubKey)
            pkcs1_15.new(pubKeyObj).verify(ballotHash, sig)
            self.transactions.append(sig)
            return True
        except (ValueError, TypeError):
            return False
        