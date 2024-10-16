from Objects.BlockObjects import *
from Crypto.Hash import SHA256

class Ballot:
    def __init__(self, name, data, identifier, author_address):
        self.name = name
        self.data = data
        self.identifier = identifier
        self.author = author_address
        self.ballot_hash = None
    
    def computeBallotHash(self):
        ballot_str = f"{self.identifier}{self.name}{self.data}{self.author}".encode()
        self.ballot_hash = SHA256.new(ballot_str)



        


