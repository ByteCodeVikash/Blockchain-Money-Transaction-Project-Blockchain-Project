from flask import Flask, jsonify, request
import hashlib
import json
import random
import sys

app = Flask(__name__)

# Hash function
def hashMe(msg=""):
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

# Make a transaction
def makeTransaction(maxValue=3):
    sign = int(random.getrandbits(1)) * 2 - 1
    amount = random.randint(1, maxValue)
    vinnyPays = sign * amount
    kinnyPays = -1 * vinnyPays
    return {'Vinny': vinnyPays, 'Kinny': kinnyPays}

# Create a block
def createBlock(txns, chain):
    parentBlock = chain[-1]
    parentHash = parentBlock['hash']
    blockNumber = parentBlock['contents']['blockNumber'] + 1
    txnCount = len(txns)
    blockContents = {'blockNumber': blockNumber, 'parentHash': parentHash, 'txnCount': txnCount, 'txns': txns}
    blockHash = hashMe(blockContents)
    block = {'hash': blockHash, 'contents': blockContents}
    return block

# Initialize blockchain and transaction buffer
chain = [{'hash': 'genesisHash', 'contents': {'blockNumber': 0, 'parentHash': None, 'txnCount': 0, 'txns': []}}]
txnBuffer = [makeTransaction() for _ in range(30)]

@app.route('/mineBlock', methods=['POST'])
def mineBlock():
    global txnBuffer
    blockSizeLimit = 5
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        txnList.append(newTxn)
    myBlock = createBlock(txnList, chain)
    chain.append(myBlock)
    return jsonify(myBlock), 200

@app.route('/getChain', methods=['GET'])
def getChain():
    return jsonify(chain), 200

@app.route('/')
def index():
    return """
    <h1>Blockchain Demo</h1>
    <a href="/mineBlock">Mine a Block</a><br>
    <a href="/getChain">View Blockchain</a>
    """

if __name__ == '__main__':
    app.run(port=5000)
