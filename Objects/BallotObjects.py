from Objects.BlockObjects import *
from Objects.AccountObjects import *
from Crypto.Hash import SHA256

class Ballot:
    def __init__(self, name, data, identifier, author: Account):
        self.name = name
        self.data = data
        self.identifier = identifier
        self.author = author.addr
        self.ballotHash = None
    
    def computeBallotHash(self):
        ballotStr = f"{self.identifier}{self.name}{self.data}{self.author}".encode()
        self.ballotHash = SHA256.new(ballotStr)



        


