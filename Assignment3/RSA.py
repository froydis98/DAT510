from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes 
import Crypto
import hashlib
from Crypto.PublicKey import RSA

def generatePrimes(bitLength):
    # Todays standard would probably be 1024 bits
    p = Crypto.Util.number.getPrime(bitLength, randfunc=get_random_bytes)
    q = Crypto.Util.number.getPrime(bitLength, randfunc=get_random_bytes)
    if p == q:
        return "p og q kan not be the same"
    n = p*q
    return p, q, n

def totient(p, q):
    return (p-1) * (q-1)

def gcd(e,phi):
    while(phi != 0):
        e, phi = phi, e % phi
    return e

#Extended Euclidean Algorithm
def eea(e, phi):
    if(e % phi == 0):
        return(phi, 0, 1)
    else:
        gcd, s, t = eea(phi, e % phi)
        s = s-((e//phi) * t)
        return(gcd,t,s)
 
#Multiplicative Inverse
def mult_inv(e,phi):
    gcd, s, _=eea(e, phi)
    if(gcd != 1):
        print('The modular inverse does not exist')
        return None
    else:
        """ if(s < 0):
            print("s=%d. Since %d is less than 0, s = s(modr), i.e., s=%d."%(s,s,s%phi))
        elif(s > 0):
            print("s=%d."%(s)) """
        return s % phi

def verifySignature(signature, message, e, n):
    ourHash = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    hashFromSignature = pow(signature, e, n)
    print(message)
    if ourHash == hashFromSignature:
        print('The signature is verified')
        return True
    else:
        print('Something went wrong, maybe there is a man in the middle? Do not trust this')
        return False

# Run main to see a staged scenario where we use a digital signature and verify it
def main():
    """ keyPair = RSA.generate(bits=1024)
    print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
    print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})") """

    p, q, n = generatePrimes(1024)

    # The message kan only be ascii signs. Do not use Æ, Ø, Å and other special characters
    message = b'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'
    messageTamp = b'Dette er en melding fra Eve, forkledd som Alice'

    phi = totient(p, q)

    # e is the public exponent, Fn = 2^2^n + 1 med n = 4
    """ for i in range(1, phi-1):
        if(gcd(i,phi)==1):
            e=i """
    
    e = 65537

    # d is the private key
    d = mult_inv(e, phi)
    # d * e = 1 mod phi(n)

    print("The public key pair is e =", e, "and n =", n)
    print("The private key pair is d =", d, "and n =", n)
    # Creates a signature
    hashedMessage = int.from_bytes(hashlib.sha256(message).digest(), byteorder='big')
    signature = pow(hashedMessage, d, n)
    # Verify the signature
    verifySignature(signature, message, e, n)
    

if __name__ == "__main__":
    main()
