from Objects.BlockObjects import *
from Objects.BallotObjects import *
from Objects.AccountObjects import * 
import unittest

class Testing(unittest.TestCase):
    
    # SET UP ACCOUNT AND BLOCKCHAIN FOR EACH TEST
    def setUp(self):
        # CREATE Account CLASS OBJECT THEN CALL generate() TO MAKE KEY PAIR & ADDRESS 
        self.myAcct = Account()
        self.myAcct.generate()

        # CREATE A Blockchain OBJECT 
        self.myChain = Blockchain()
        self.genesisBlock = self.myChain.getBlockByIndex(0)

    # TEST PROPERTIES OF GENESIS BLOCK
    def testGenesisBlock(self):
        self.assertEqual(self.genesisBlock.getBlockIndex(), 0)
        self.assertEqual(self.genesisBlock.getBlockPreviousHash(), "0")
        self.assertIsInstance(self.genesisBlock.getBlockNonce(), int)
        self.assertIsInstance(self.genesisBlock.getBlockTimestamp(), float)

    # TEST CREATING OF BALLOT HASH, NO FUNCTIONALITY FOR PASSING A DOCUMENT THROUGH BALLOT OBJECT
    def testCreateBallot(self):
        ballot = Ballot('Test Ballot', 'someDocument', '1234', self.myAcct.addr)
        ballot.computeBallotHash()
        self.assertIsNotNone(ballot.getBallotHash())

    def testBallotSigning(self):
        ballot = Ballot('Test Ballot', 'someDocument', '1234', self.myAcct.addr)
        ballot.computeBallotHash()

        # CREATE VoteTransaction OBJECT AND SIGN 
        self.myAcct.createVoteTransactionObject(ballot, "yes")
        self.myAcct.createAndSignTx(ballot, "yes")

        account_transactions = self.myAcct.getTransactions()
        nonce = self.myAcct.getNonce()
        self.assertIsNotNone(account_transactions[nonce])

    # TEST PoW
    def testPoW(self):
        ballot = Ballot("Abortion", "yes or no", "2", self.myAcct)
        ballot.computeBallotHash()

        # CREATE VoteTransaction OBJECT AND SIGN
        self.myAcct.createVoteTransactionObject(ballot, "yes")
        self.myAcct.createAndSignTx(ballot, "yes")
        account_transactions = self.myAcct.getTransactions()
        sig = account_transactions[1]

        # CREATE A NEW BLOCK
        newBlock = Block("1", self.myChain.getLatestBlock().getBlockHash(), sig, time.time(), 1)

        # CHECK INITAL HASH BEFORE PoW
        initialHash = newBlock.getBlockHash()
        self.assertIsNotNone(initialHash)
        
        # DO PoW ON BLOCK
        self.myChain.proofOfWork(newBlock)
        postHash = newBlock.getBlockHash()

        # CHECK THAT HASH DIFFERS AFTER PoW 
        self.assertNotEqual(initialHash, postHash)
        
        # ADD PoW BLOCK TO CHAIN
        self.myChain.addBlock(newBlock)

        # TEST CHAIN PROPERTIES
        genesis_block = self.myChain.getBlockByIndex(0)
        genesis_block_hash = genesis_block.getBlockHash()

        added_block = self.myChain.getLatestBlock()
        added_block_previous_hash = added_block.getBlockPreviousHash()

        self.assertEqual(genesis_block_hash, added_block_previous_hash)
        
    
    def testTransactionModificationInvalidatesSignature(self):
        ballot = Ballot('Proposition', 'Document', '5678', self.myAcct.addr)
        ballot.computeBallotHash()
        self.myAcct.createVoteTransactionObject(ballot, "yes")
        self.myAcct.createAndSignTx(ballot, "yes")
        
        # MODIFY BALLOT AFTER SIGNING
        ballot.setBallotData('Tampered Hash')
        ballot.computeBallotHash()
        
        # ENSURE VERIFICATION FAILS
        account_transactions = self.myAcct.getTransactions()
        nonce = self.myAcct.getNonce()
        tx = account_transactions[nonce]
        self.assertFalse(self.myAcct.verifyTx(ballot.getBallotHash(), tx))


if __name__ == 'main':
    unittest.main()
