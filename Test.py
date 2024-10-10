from Objects.BlockObjects import *
from Objects.BallotObjects import *
from Objects.AccountObjects import * 
from Objects.TransactionObjects import *
import unittest

class Testing(unittest.TestCase):
    
    # SET UP ACCOUNT AND BLOCKCHAIN FOR EACH TEST
    def setUp(self):
        self.myAcct = Account()
        self.myAcct.generate()

        self.myChain = Blockchain()
        self.genBlock = self.myChain.chain[0]



    # TEST PROPERTIES OF GENESIS BLOCK
    def testGenesisBlock(self):
        self.assertEqual(self.genBlock.index, 0)
        self.assertEqual(self.genBlock.prevHash, "0")
        self.assertIsInstance(self.genBlock.nonce, int)
        self.assertIsInstance(self.genBlock.timestamp, float)


    # TEST BALLOT CREATION AND SIGNING
    def testBallotCnS(self):
        ballot = Ballot("Abortion", "yes or no", "2", self.myAcct)
        ballot.computeBallotHash()

        # CREATE A TRANSACTION OBJECT TO SIGN
        tx = Transaction(self.myAcct, ballot, "yes")
        tx.setupTx()
        
        # SIGN TX 
        tx.signTx(self.myAcct)

        # CHECK THAT SIG WAS CREATED AND ADDED TO TX LIST
        self.assertEqual(len(self.myAcct.transactions), 1)
        sig = self.myAcct.transactions[0]
        self.assertIsNotNone(tx.txSig)

    # TEST PoW
    def testPoW(self):
        ballot = Ballot("Abortion", "yes or no", "2", self.myAcct)
        ballot.computeBallotHash()

        self.myAcct.signBallot(ballot.ballotHash, "2", "Abortion", "yes or no", self.myAcct.addr)
        sig = self.myAcct.transactions[0]
        newBlock = Block("1", self.myChain.getLatestBlock(), sig, time.time(), 1)

        # CHECK INITAL HASH BEFORE PoW
        initialHash = newBlock.hash
        self.assertIsNotNone(initialHash)
        
        self.myChain.proofOfWork(newBlock)
        postHash = newBlock.hash

        self.assertNotEqual(initialHash, postHash)
        self.myChain.addBlock(newBlock)

        recentBlock = self.myChain.getLatestBlock()
        self.assertEqual(recentBlock.index, '1')
        self.assertEqual(recentBlock.prevHash, self.genBlock.hash)
        self.assertEqual(recentBlock.hash, newBlock.hash)

if __name__ == 'main':
    unittest.main()
