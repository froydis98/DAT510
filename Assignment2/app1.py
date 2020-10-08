from flask import Flask, render_template, request, redirect, url_for
from SDES import SDES, frombits
from SecureCommunication import publicKey, sharedKey, CSPRNG_BBS
import requests, json

# This server represents Bob's side of the communication

app = Flask(__name__)

# The predefined values that both Alice and Bob knows
g = 2
sharedPrime = 683

# Bob's private key, which is secret
bobPrivate = 131

secretKeyBit = ""
encrypted = ''

# The first page, which is just informative and links you to create the secret key with Alice
@app.route('/')
def index():
    return '<h1>Hi Bob, this is a page where you can communicate with Alice through a secure channel</h1><h2>To connect to Alice, <a href="/getPub">click here</a>'

# Going to this page will automaticly fetch Alice's public key and create the secret key and a secure communication
@app.route('/getPub', methods=['GET'])
def getPub():
    alicePub = requests.get("http://127.0.0.1:3000/sendPub")
    if alicePub:
        shared = sharedKey(int(alicePub.text), bobPrivate, sharedPrime)
        global secretKeyBit
        secretKeyBit = CSPRNG_BBS(shared, 10)
        secretKey = int(secretKeyBit, 2)
        return "<h2>You now have a secure connection with Alice, if you want to send a message <a href='/sendMsg'>click here </a></h2>"
    else:
        return 'No response'

# This page is for Alice to fetch so she get's Bob's public key
@app.route('/sendPub')
def generatePublicKey():
    return f'{publicKey(bobPrivate, g, sharedPrime)}'

# At this page you can write in a message and send it to Alice.
# There can only be one message sent at a time.
# Before the message is sent, it is encrypted by using SDES from Assignment 1 and the shared secret key
@app.route('/sendMsg', methods=['POST', 'GET'])
def sendMessage():
    if secretKeyBit == '':
        return "You do not have a secure connection with Alice. Go to <a href='/getPub'> /getPub </a> to connect"
    text = request.form.get('message')
    if text:
        messageBits = ' '.join(format(ord(x), 'b').zfill(8) for x in text).split(' ')
        global encrypted
        encrypted = ''
        for i in range(0, len(text)):
            encrypted += (SDES(messageBits[i], secretKeyBit))
    return render_template('sendMsg.html', title="Send message")

# This page is for Alice to fetch to see if Bob have sent any messages
@app.route('/sentMsg')
def sentMessage():
    global encrypted
    return encrypted

# Here we fetch Alice's message if there is some and decrypt it.
@app.route('/getMsg', methods=['GET'])
def getMessage():
    if secretKeyBit == '':
        return 'You do not have a secure connection with Alice, go to http://127.0.0.1:5000/getPub'
    encryptedText = requests.get("http://127.0.0.1:3000/sentMsg")
    if encryptedText:
        encrypted = encryptedText.text
        encryptedList = [encrypted[i:i+8] for i in range(0, len(encrypted), 8)]
        decrypted = ''
        for i in range (0, len(encryptedList)):
            decrypted += frombits(SDES(encryptedList[i], secretKeyBit, True))
        if decrypted == '':
            return "There is no message, if you want to write a message, <a href='/sendMsg'>click here</a>"
        return '''The message from Alice is: <h3>{}</h3> If you want to answer, go to <a href='/sendMsg'>/sendMsg</a>'''.format(decrypted) 
    else:
        return "There is no message"

# We run this server at port 5000 so it does not crash or overwrite the other server
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)
