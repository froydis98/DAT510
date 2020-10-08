from flask import Flask, render_template, request, redirect, url_for
from SDES import SDES, frombits
from SecureCommunication import publicKey, sharedKey, CSPRNG_BBS
import requests

app = Flask(__name__)

g = 2
sharedPrime = 683
alicePrivate = 217

secretKeyBit = ""
encrypted = ''

@app.route('/')
def index():
    return '<h1>Hi Alice, this is a page where you can communicate with Bob through a secure channel</h1><h2>To connect to Bob, <a href="/getPub">click here</a>'

@app.route('/getPub', methods=['GET'])
def getPub():
    bobPub = requests.get("http://127.0.0.1:5000/sendPub")
    if bobPub:
        shared = sharedKey(int(bobPub.text), alicePrivate, sharedPrime)
        global secretKeyBit 
        secretKeyBit = CSPRNG_BBS(shared, 10)
        secretKey = int(secretKeyBit, 2)
        return "<h2>You now have a secure connection Bob, if you want to send a message <a href='/sendMsg'>click here </a></h2>"
    else:
        return 'No response, could not connect Bob'

@app.route('/sendPub')
def generatePublicKey():
    return f'{publicKey(alicePrivate, g, sharedPrime)}'

@app.route('/sendMsg', methods=['POST', 'GET'])
def sendMessage():
    if secretKeyBit == '':
        return "You do not have a secure connection with Bob. Go to <a href='/getPub'> /getPub </a> to connect"
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
        return 'You do not have a secure connection with Bob, go to <a href="/getPub">/getPub</a>'
    encryptedText = requests.get("http://127.0.0.1:5000/sentMsg")
    if encryptedText:
        encrypted = encryptedText.text
        encryptedList = [encrypted[i:i+8] for i in range(0, len(encrypted), 8)]
        decrypted = ''
        for i in range (0, len(encryptedList)):
            decrypted += frombits(SDES(encryptedList[i], secretKeyBit, True))
        if decrypted == '':
            return "There is no message, if you want to write a message, <a href='/sendMsg'>click here</a>"
        return '''The message from Bob is: <h3>{}</h3> If you want to answer, go to <a href='/sendMsg'>/sendMsg</a>'''.format(decrypted) 
    else:
        return "There is no message"


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=3000, debug=True)
