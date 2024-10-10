from Objects.AccountObjects import Account
from Objects.BallotObjects import Ballot
import time
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA




class Transaction:
    def __init__(self, account: Account, ballot: Ballot, vote: str):
        self.pubKey = account.pubKey
        self.nonce = account.nonce
        self.ballotHash = ballot.ballotHash
        if vote == 'yes' or vote == 'no':
            self.vote = vote
        else: raise(ValueError) 

    def setupTx(self):

        # GENERATE A HASH FOR TX DETAILS
        hashStr = f"{self.ballotHash}{self.vote}{self.nonce}{time.time()}".encode()
        self.txHash = SHA256.new(hashStr)

    def signTx(self, account: Account):
        
        # SIGN OFF ON TRANSACTION
        sig = pkcs1_15.new(account.key).sign(self.txHash)

        # VERIFY SIGNATURE
        try:
            pubKeyObj = RSA.import_key(self.pubKey)
            pkcs1_15.new(pubKeyObj).verify(self.txHash, sig)
            self.txSig = sig

            # INCREASE ACCOUNT NONCE
            account.nonce += 1
            account.transactions.append(self)
            return True 
        except (ValueError, TypeError):
            return False


