# Assignment 1

## Part 1
Vigenere cipher decrypter. Execute it as a normal python file.
One way to execute it is by using your command line.
```
python .\Part1\VigenereCipher.py
```

## Part 2
SDES and tripleSDES. Execute it as a normal python file.
Same as part 1, use the command line.
```
python .\Part2\SDES.py
```
As default this file does not return anything. But if you want to test the different functions you can for example add the lines:
```
print(bruteForceSDES(message1))
print(bruteForceTripleSDES(message2))
```

To execute the app.py file you need flask. Make sure you have pip. If you don't have pip or are unsure, look here https://phoenixnap.com/kb/install-pip-windows.

When you are sure you have pip, we can install flask like this.
In your command line:
```
pip install flask
```
Then you can start the application:
```
python .\Part2\app.py
```

Go to the url: http://127.0.0.1:5000/0101110101010111110111001101110001010100

Try to insert your own bits in the url and see what the deciphered message is. This prefilled message says 'Hello'
