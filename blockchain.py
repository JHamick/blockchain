import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask

class blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        
        # Creating the genesis block
        self.new_block(previous_has=1, proof=100)
        
    def new_block(self):
        #Creates a new block and adds it to the chain
        """
        Creates a new block in the blockchain
        Args:
            proof (int): The proof given by the proof of work algorithm
            previous_hash: (str) Hash of previous block
            return (dict): New Block
        """
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp':  time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        
        # Resets current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block
        
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
        """
        Creates a SHA-256 hash of a block
        Args:
            block (dict): The block (WOW!)
            return (str)
        """
        # Makes sure the dictionary is ordered as not to have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1] 

    def proof_of_work(self, last_proof):
        """
        Simple proof of work alogrithm:
        Find a number p' such that hash(pp') contains leading 4 zeros where p is the previous p'
        p is the previous proof, and p' is the new proof
        Args:
            last_proof (int)
            return (int)
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does has(last_proof, proof) contain 4 leading zeros?
        Args:
            last_proof (int) Previous proof
            proof (int) Current proof
            return (bool) True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hast = hashlib.sha256(guess).hexdigest()
        return guess_has[:4] = "0000"

# Instantiate our node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-','')

# Instantiate the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    #Check that required fields are in the POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response, 200)

if __name__ = '__main__':
    app.run(host='0.0.0.0', port=5000)

