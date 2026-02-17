import hashlib
import json
from time import time

class blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    def new_block(self):
        #Creates a new block and adds it to the chain
        pass
        
    def  new_transaction(self, sender, recipient, amount):
    #Adds a new transaction to the list of transactions
        """
        Creates a new transaction
        Args:
            sender (str): Address of the sender
            recipient (str): Address of the recipient
            amount (int): Amount sent
            return (int): The index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass