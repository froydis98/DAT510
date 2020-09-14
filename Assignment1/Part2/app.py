from flask import Flask
import SDES

app = Flask(__name__)

key1 = '1000101110'
key2 = '0110101110'


@app.route('/<input>')
def decrypt(input):
    start = 0
    message = ''
    for i in range(int(len(input)/8)):
        decrypted = SDES.tripleSDES(input[start:start+8], key1, key2, True)
        message += SDES.frombits(decrypted)
        start += 8
    return message

if __name__ == "__main__":
    app.run()