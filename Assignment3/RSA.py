from Crypto.Random import get_random_bytes 
import Crypto
import hashlib
from Crypto.PublicKey import RSA
from math import gcd
import timeit
import random

def generatePrimes(bitLength):
    p, q = 0, 0
    # Todays standard is 1024 bits and larger
    while p == q:
        p = Crypto.Util.number.getPrime(bitLength, randfunc=get_random_bytes)
        q = Crypto.Util.number.getPrime(bitLength, randfunc=get_random_bytes)
    n = p*q
    return p, q, n

def totient(p, q):
    return (p-1) * (q-1)

def generatePublicKey(phi):
    while True:
        rand = random.randint(3, phi-1)
        if (gcd(rand, phi) == 1 and phi % rand != 0):
            return rand
    return "Did not find any e"
        
# Code from https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
# Returns modulo inverse of a with 
# respect to m using extended Euclid 
# Algorithm Assumption: a and m are 
# coprimes, i.e., gcd(a, m) = 1 
def modInverse(a, m) :
    m0 = m 
    y = 0
    x = 1
    if (m == 1) : 
        return 0
    while (a > 1) : 
        # q is quotient 
        q = a // m 
        t = m 
        # m is remainder now, process 
        # same as Euclid's algo 
        m = a % m 
        a = t 
        t = y 
        # Update x and y 
        y = x - q * y 
        x = t 
    # Make x positive 
    if (x < 0) : 
        x = x + m0 
    return x 
    # This code is contributed by Nikita tiwari. 


# Check that the signature is correct to the message
def verifySignature(signature, message, e, n):
    print("\n The reciever checks the signature.")
    ourHash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, e, n)
    print('The hash the signature is created from: ', hashFromSignature)
    print('Our recreated hash from the message: ', ourHash)
    if ourHash == hashFromSignature:
        print('The signature is verified \n')
        return True
    else:
        print('Something went wrong, maybe there is a man in the middle? Do not trust this \n')
        return False

# Run main to see a staged scenario where we use a digital signature and verify it
def main():
    # Added timer to see the differences on runtime with smaller and bigger keys
    start_time = timeit.default_timer()

    # Generate the prime numbers, choose bit length
    p, q, n = generatePrimes(512)

    # The message kan only be ascii signs. Do not use Æ, Ø, Å and other special characters
    message = b'This is a message from Alice to Bob'   
    messageTamp = b'This is a message from Alice to Bob, but Eve has tampered it'

    # Phi is the totient of p and q
    phi = totient(p, q)

    # e is the public exponent
    # e is often 65537 (Fn = 2^2^n + 1 med n = 4), but since we want to test different numbers here I won't use it
    e = generatePublicKey(phi)

    # d is the private key
    d = modInverse(e, phi)
    # d * e = 1 mod phi(n)

    print("The public key pair is e =", e, "and n =", n)
    print("\n The private key pair is d =", d, "and n =", n)
    print('\n The message is: ', message)

    # Creates a signature
    hashedMessage = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    print("\n The hashed message is:", hashedMessage)
    signature = pow(hashedMessage, d, n)
    print("\n The signature created from the hashed message:", signature)

    # Verify the signature
    verifySignature(signature, message, e, n)

    # remove the comment signs below if you want to test the tampered message
    """ # Try to verify the signature on the tampered message
    verifySignature(signature, messageTamp, e, n) """

    elapsed = timeit.default_timer() - start_time
    print("This program used:", elapsed, "sec to run")

if __name__ == "__main__":
    main()
