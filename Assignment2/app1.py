from flask import Flask, render_template, request, redirect, url_for
from SDES import SDES, frombits
from SecureCommunication import publicKey, sharedKey, CSPRNG_BBS
import requests, json

app = Flask(__name__)

g = 2
sharedPrime = 683
bobPrivate = 131

secretKeyBit = ""
encrypted = ''

@app.route('/')
def index():
    return '<h1>Hi Bob, this is a page where you can communicate with Alice through a secure channel</h1><h2>To connect to Alice, <a href="/getPub">click here</a>'

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

@app.route('/sendPub')
def generatePublicKey():
    return f'{publicKey(bobPrivate, g, sharedPrime)}'

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

@app.route('/sentMsg')
def sentMessage():
    global encrypted
    return encrypted

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

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)
