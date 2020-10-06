from flask import Flask, jsonify
from SDES import SDES
from SecureCommunication import publicKey, sharedKey, CSPRNG_BBS
import requests, json

app = Flask(__name__)

g = 2
sharedPrime = 683
bobPrivate = 131

@app.route('/getPub', methods=['GET'])
def index():
    alicePub = requests.get("http://127.0.0.1:3000/sendPub")
    if alicePub:
        shared = sharedKey(int(alicePub.text), bobPrivate, sharedPrime)
        secretKeyBit = CSPRNG_BBS(shared, 10)
        secretKey = int(secretKeyBit, 2)
        return "Secure connection"
    else:
        return 'No response'

@app.route('/sendPub')
def generatePublicKey():
    return f'{publicKey(bobPrivate, g, sharedPrime)}'

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)
