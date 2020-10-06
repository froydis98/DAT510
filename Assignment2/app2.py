from flask import Flask, jsonify
from SDES import SDES
from SecureCommunication import publicKey, sharedKey, CSPRNG_BBS
import requests

app = Flask(__name__)

g = 2
sharedPrime = 683
alicePrivate = 217

@app.route('/getPub', methods=['GET'])
def index():
    bobPub = requests.get("http://127.0.0.1:5000/sendPub")
    if bobPub:
        shared = sharedKey(int(bobPub.text), alicePrivate, sharedPrime)
        secretKeyBit = CSPRNG_BBS(shared, 10)
        secretKey = int(secretKeyBit, 2)
        return "Secure connection"
    else:
        return 'No response'

@app.route('/sendPub')
def generatePublicKey():
    return f'{publicKey(alicePrivate, g, sharedPrime)}'

@app.route('/sendMsg/<input>')
def sendMessage(input):
    return input

@app.route('/getMsg/')
def getMessage():
    


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=3000, debug=True)
