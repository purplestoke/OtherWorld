from BlockObjects import *
from BallotObjects import *
from AccountObjects import * 

myAcct = Account()
myAcct.generate()


MyChain = Blockchain()
print(MyChain.chain[0])

ballot = Ballot("Abortion", "yes or no", "2", myAcct)
ballot.computeBallotHash()

myAcct.signBallot(ballot.ballotHash, "2", "Abortion", "yes or no", myAcct.addr)

sig = myAcct.transactions[0]

newBlock = Block("1", MyChain.getLatestBlock(), sig, time.time(), 1)
MyChain.addBlock(newBlock)

print(MyChain.chain)