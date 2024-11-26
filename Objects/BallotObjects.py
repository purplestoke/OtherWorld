from Objects.BlockObjects import *
from Crypto.Hash import SHA256
from pymerkle import InmemoryTree as MerkleTree
import fitz

"""
HOLDS BALLOT DOCUMENT
ballot_hash ACTS AS A POINTER FOR THE BALLOT OBJECT
HASH ENSURES THE BALLOT IS AUTHENTIC AS ANY CHANGES TO THE DOCUMENT
WOULD RESULT IN CHANGES TO THE ballot_hash
"""

class Ballot:
    def __init__(self, name, data, identifier, author_address):
        self.__name = name
        self.__data = data
        self.__identifier = identifier
        self.__author = author_address
        self.__ballot_hash = None
    
    def computeBallotHash(self):
        ballot_str = f"{self.__identifier}{self.__name}{self.__data}{self.__author}".encode()
        self.__ballot_hash = SHA256.new(ballot_str) 

    def getBallotHash(self):
        return self.__ballot_hash
    
    def getBallotData(self):
        return self.__data
    
    def getBallotIdentifier(self):
        return self.__identifier
    
    def getBallotAuthor(self):
        return self.__author
    
    def getBallotName(self):
        return self.__name
    
    def setBallotData(self, data):
        self.__data = data