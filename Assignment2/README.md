# Assignment 2

## Part 1
The file SecureCommunication.py contains part 1 of the assignment. 
Execute it as a normal python file.
One way to execute it is by using your command line.
```
python .\SecureCommunication.py
```

This will print out all the steps in the process of creating the key. 
You can choose to send a predefined message to Bob, or you can write your own message.


## Part 2
To execute the app  files you need flask. Make sure you have pip. If you don't have pip or are unsure, look here https://phoenixnap.com/kb/install-pip-windows.

When you are sure you have pip, we can install flask like this.
In your command line:
```
pip install flask
```

Then you can start the application app1.py which is Bob's server.
```
python .\app1.py
```
This app will be at port 5000. http://127.0.0.1:5000

To start Alice's server, you use the command:
```
python .\app2.py
```
This should be done in another terminal, so that they don't overwrite each other. I would recommend running one app on PowerShell and one on Bash. 
Alice's server will be at port 3000. http://127.0.0.1:3000

You can follow the instructions on the web page, or follow the steps here:

Go to /getPub to create the secure communication with the other part.

After generating the secret key:

Go to /sendMsg to send messages to the other part

Go to /getMsg to see if you have gotten any messages from the other part
