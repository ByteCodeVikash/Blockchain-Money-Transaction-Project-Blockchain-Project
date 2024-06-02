from flask import Flask, render_template, jsonify, request, redirect, url_for
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def mine():
    return render_template('mine.html')

@app.route('/mine_block', methods=['POST'])
def mine_block():
    block = blockchain.mine()
    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return render_template('mine.html', block=response)

@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'POST':
        sender = request.form['sender']
        recipient = request.form['recipient']
        amount = request.form['amount']

        index = blockchain.new_transaction(sender, recipient, int(amount))
        return redirect(url_for('new_transaction'))
    return render_template('transaction.html')

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return render_template('chain.html', chain=response)

if __name__ == '__main__':
    app.run(debug=True)
