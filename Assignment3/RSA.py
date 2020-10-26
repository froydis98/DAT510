from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes 
import Crypto
import hashlib
from Crypto.PublicKey import RSA

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
    print(ourHash, hashFromSignature)
    if ourHash == hashFromSignature:
        print('The signature is verified')
        return True
    else:
        print('Something went wrong, maybe there is a man in the middle? Not trust this')
        return False


def main():
    keyPair = RSA.generate(bits=1024)
    print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
    print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
    # Decide how many bits we want our primes to be
    bits = 1024
    # Todays standard would probably be 1024 bits
    p = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
    q = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
    print(p)
    print(q)
    if p == q:
        return "p og q kan not be the same"
    n = p*q

    message = b'Dette er en melding fra Alice'
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


""" # Encrypt bytes
    cipher = pow(message,e, n)
    print("The cipher is:", cipher)
    # Decrypt bytes
    decipher = pow(cipher,d ,n)
    plaintext = long_to_bytes(decipher).decode('utf-8')
    print("The plaintext after decrypting the cipher: ", plaintext) """
    

if __name__ == "__main__":
    main()
