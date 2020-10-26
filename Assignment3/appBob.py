from flask import Flask, render_template, request, redirect, url_for
import requests, json
from RSA import generatePrimes, totient, mult_inv, verifySignature
import hashlib

# Bob's server

app = Flask(__name__)

message = ''
signature = 0
e = 65537
p, q, n = generatePrimes(1024)
phi = totient(p, q)
d = mult_inv(e, phi)

# At this page you can write in a message and send it to Alice.
# There can only be one message sent at a time.
@app.route('/', methods=['POST', 'GET'])
def sendMessage():
    text = request.form.get('message')
    if text:
        global signature
        global message
        # Hash the message and use RSA encryption to create a digital signature
        hashedMessage = int.from_bytes(hashlib.sha256(text.encode()).digest(), byteorder='big')
        signature = pow(hashedMessage, d, n)
        message = text
    return render_template('sendMsg.html', title="Send message")

# This page is for Alice to fetch to see if Bob have sent any messages
@app.route('/sentMsg')
def sentMessage():
    global message, signature, e, n
    fullMessage = {'message': message, 'signature': signature, 'e': e, 'n': n}
    return fullMessage

# Here we fetch a message from Alice's server and check that it was Alice that last edited the message.
@app.route('/getMsg', methods=['GET'])
def getMessage():
    fullMessage = {}
    fullMessage = requests.get("http://127.0.0.1:5000/sentMsg")
    messageObject = json.loads(fullMessage.content.decode())
    print(messageObject)
    if fullMessage.ok:
        if messageObject['message'] == '' or messageObject['signature'] == 0:
            return "There is no message."
        if verifySignature(messageObject['signature'], messageObject['message'].encode(), messageObject['e'], messageObject['n']):
            return '''The message from Alice is: <h3>{}</h3> <div>This message has Alice's digital signature</div>'''.format(messageObject['message'])
        return '''The message from Alice is: <h3>{}</h3> <div> But something went wrong. There might be a man in the middle here.</div>'''.format(messageObject['message']) 
    else:
        return "No response"


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=3000, debug=True)
