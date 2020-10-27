# Assignment 3

## RSA.py
Before you can execute the code you might need to install pycrypto, this is done by using the command:
```
pip install pycrypto
```

Execute the code as a normal python file. For example:
```
python .\RSA.py
```

See the result printed in the terminal.
To test a message that does not have a matching signature to the message, remove the comments on line 100 to 101.

## Flask applications
To execute the app  files you need flask. Make sure you have pip. If you don't have pip or are unsure, look here https://phoenixnap.com/kb/install-pip-windows.

When you are sure you have pip, we can install flask like this.
In your command line:
```
pip install flask
```

Then you can start the application app1.py which is Alice's server.
```
python .\appAlice.py
```
This app will be at port 5000. http://127.0.0.1:5000

To start Bob's server, you use the command:
```
python .\appBob.py
```
This should be done in another terminal, so that they don't overwrite each other. I would recommend running one app on PowerShell and one on Bash. 
Bob's server will be at port 3000. http://127.0.0.1:3000

Send a message on the starting page and go to /getMsg to see received messages and if the signature was verified.