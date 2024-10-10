from BlockObjects import *
from BallotObjects import *
from AccountObjects import * 

myAcct = Account()
myAcct.generate()


MyChain = Blockchain()
genBlock = MyChain.chain[0]
print(f"Block Nonce: {genBlock.nonce}\nBlock Index: {genBlock.index}\nTimestamp: {genBlock.timestamp}\nPrevious Block Hash: {genBlock.prevHash}\nData: {genBlock.data}")

ballot = Ballot("Abortion", "yes or no", "2", myAcct)
ballot.computeBallotHash()

myAcct.signBallot(ballot.ballotHash, "2", "Abortion", "yes or no", myAcct.addr)

sig = myAcct.transactions[0]

newBlock = Block("1", MyChain.getLatestBlock(), sig, time.time(), 1)
MyChain.addBlock(newBlock)

recentBlock = MyChain.getLatestBlock()
print(f"Block Nonce: {recentBlock.nonce}\nBlock Index: {recentBlock.index}\nTimestamp: {recentBlock.timestamp}\nPrevious Block Hash: {recentBlock.prevHash}\nData: {recentBlock.data}")
