from flask import Flask, render_template, request, redirect, url_for
import requests, json

# Bob's server

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hei Bob</h1>'



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000, debug=True)
