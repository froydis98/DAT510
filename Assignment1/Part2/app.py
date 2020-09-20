from flask import Flask
from SDES import tripleSDES, frombits

app = Flask(__name__)

key1 = '1000101110'
key2 = '0110101110'


#0101110101010111110111001101110001010100 will give Hello
@app.route('/<input>')
def decrypt(input):
    start = 0
    message = ''
    for i in range(int(len(input)/8)):
        decrypted = tripleSDES(input[start:start+8], key1, key2, True)
        message += frombits(decrypted)
        start += 8
    return message

if __name__ == "__main__":
    app.run()
