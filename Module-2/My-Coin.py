# Module -2 Create a Cryptocurrency

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests

## Building the blockchain
class Blockchain:
    
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1, previous_hash='0')
    
    
    def create_block(self, proof, previous_hash):
        block={'index': len(self.chain)+1,
               'timestamp': str(datetime.datetime.now()),
               'proof' : proof,
               'previous_hash':previous_hash}
        self.chain.append(block)
        return block
    
    
    def return_previous_block(self):
        return self.chain[-1]
    
    
    def proof_of_work(self, previous_proof):
        check_proof=False
        new_proof=1
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] =='0000':
                check_proof=True
            else:
                new_proof+=1
        
        return new_proof
    
    def hash(self, block):
        encoded_block=json.dumps(block, sort_keys=True).encode()
        hash_operation=hashlib.sha256(encoded_block).hexdigest()
        return hash_operation
        
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
 

           
##Mining Blockchain


##Create a Web App
app=Flask(__name__)

##Create blockchain
blockchain=Blockchain()


##Mining Block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block=blockchain.return_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash)
    response={'message':'Congratulations! You just mined a new block!',
              'index': block['index'],
              'timestamp': block['timestamp'],
              'proof': block['proof'],
              'hash': str(blockchain.hash(block)),
              'previous_hash': block['previous_hash']}
    return jsonify(response),200



##Getting the full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,
              'length': len(blockchain.chain)}
    return jsonify(response), 200



@app.route('/is_valid',methods=['GET'])
def is_valid():
    if blockchain.is_chain_valid(blockchain.chain):
        response={'message': 'Congratulation! your chain is valid!'
                }
    else:
        response={'message':'Oops! your chain is invalid!'
                }
    return jsonify(response), 200




## Decentralising our blockchain
##Running the app
app.run(host='0.0.0.0')
app.debug=True