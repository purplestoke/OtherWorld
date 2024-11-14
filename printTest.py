from Objects.BlockObjects import *
from Objects.BallotObjects import *
from Objects.AccountObjects import * 

blockchain = Blockchain()

user = Account()
user.generate()

ballot = Ballot("Abortion Ban", "someDoc", "12", user.getPubKey())

user.createVoteTransactionObject(ballot, 'yes')
user.createAndSignTx(ballot, 'yes')

user_transactions = user.getTransactions()
mock_transaction = user_transactions[1]

#for k, v in user_transactions.items():
#     print(f"Nonce: {k}\nSignature: {v}")

previous_block = blockchain.getLatestBlock()
previous_hash = previous_block.getBlockHash()


new_block = Block(1, previous_hash, mock_transaction, time.time())
new_block_current_hash = new_block.getBlockHash()
#print(f"Hash before PoW {new_block_current_hash}")

pow_hash = blockchain.proofOfWork(new_block)
#print(f"Hash after PoW {pow_hash}") 

blockchain.addBlock(new_block)
#print("Block Added!")

the_blockchain = blockchain.getChain()

contents = {}
i = 1
for blk in the_blockchain:
    info = blk.getContents()
    contents[i] = info
    i += 1

print(contents)