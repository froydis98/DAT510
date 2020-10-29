from flask import Flask, render_template, request, redirect, url_for
import requests, json
from RSA import generatePrimes, totient, modInverse, verifySignature, generatePublicKey
import hashlib
from math import gcd

# Alice's server

app = Flask(__name__)

message = ''
signature = 0
e = 0
n = 0

# At this page you can write in a message and send it to Bob.
# There can only be one message sent at a time.
@app.route('/', methods=['POST', 'GET'])
def sendMessage():
    text = request.form.get('message')
    if text:
        global signature, message, e, n
        # Hash the message and use RSA encryption to create a digital signature
        hashedMessage = int.from_bytes(hashlib.sha256(text.encode()).digest(), byteorder='big')
        # Generate the keys, does this here because we want new keys for each message
        p, q, n = generatePrimes(512)
        phi = totient(p, q)
        e = generatePublicKey(phi)
        d = modInverse(e, phi)

        # Creates signature for the message
        signature = pow(hashedMessage, d, n)
        message = text
    return render_template('sendMsg.html', title="Send message")

# This page is for Bob to fetch to see if Alice have sent any messages
@app.route('/sentMsg')
def sentMessage():
    global message, signature, e, n
    fullMessage = {'message': message, 'signature': signature, 'e': e, 'n': n}
    return fullMessage

# Here we fetch a message from Bob's server and check that it was Bob that last edited the message.
@app.route('/getMsg', methods=['GET'])
def getMessage():
    fullMessage = {}
    fullMessage = requests.get("http://127.0.0.1:3000/sentMsg")
    messageObject = json.loads(fullMessage.content.decode())
    if fullMessage.ok:
        if messageObject['message'] == '' or messageObject['signature'] == 0:
            return "There is no message."
        # If there is a message, check that the signature matches to the message
        if verifySignature(messageObject['signature'], messageObject['message'].encode(), messageObject['e'], messageObject['n']):
            return '''The message from Bob is: <h3>{}</h3> <div>This message has Bob's digital signature</div>'''.format(messageObject['message'])
        return '''The message from Bob is: <h3>{}</h3> <div> But something went wrong. There might be a man in the middle here.</div>'''.format(messageObject['message']) 
    else:
        return "No response"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)