from flask import Flask, render_template, request, redirect, url_for
import requests, json

# Alice's server

app = Flask(__name__)

message = ''
signature = 0

@app.route('/')
def index():
    return '<h1>Hei Alice</h1>'

# At this page you can write in a message and send it to Alice.
# There can only be one message sent at a time.
# Before the message is sent, it is encrypted by using SDES from Assignment 1 and the shared secret key
@app.route('/sendMsg', methods=['POST', 'GET'])
def sendMessage():
    text = request.form.get('message')
    if text:
        global message
        message = text
    return render_template('sendMsg.html', title="Send message")

# This page is for Bob to fetch to see if Alice have sent any messages
@app.route('/sentMsg')
def sentMessage():
    global message, signature
    return message, signature

# Here we fetch Bob's message if there is some and decrypt it.
@app.route('/getMsg', methods=['GET'])
def getMessage():
    message, signature = requests.get("http://127.0.0.1:3000/sentMsg")
    if message:
        if message == '' or signature == 0:
            return "There is no message, if you want to write a message, <a href='/sendMsg'>click here</a>"
        return '''The message from Bob is: <h3>{}</h3> If you want to answer, go to <a href='/sendMsg'>/sendMsg</a>'''.format(message) 
    else:
        return "No response"

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)