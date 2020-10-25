from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes 
import Crypto

def totient(p, q):
    return (p-1) * (q-1)

def findCorrectPrimeGCD(n, phi):
    for num in range(n, 2, -1):
        for i in range(2, num):
            if (num % i) == 0:
                break
        else: 
            for i in range(1, phi+1): 
                if((num % i == 0) and (phi % i == 0)): 
                    gcd = i
                if(gcd == 1):
                    return num

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        print('The modular inverse does not exist')
    else:
        return x % m

def generateKeys(p, q, n):
    phi = totient(p, q)
    e = findCorrectPrimeGCD(n, phi)
    d = modinv(e, phi)
    return phi, e, d

def egcd(e,phi):
    while(phi!=0):
        e,phi=phi,e%phi
    return e

#Extended Euclidean Algorithm
def eea(a,b):
    if(a%b==0):
        return(b,0,1)
    else:
        gcd,s,t = eea(b,a%b)
        s = s-((a//b) * t)
        return(gcd,t,s)
 
#Multiplicative Inverse
def mult_inv(e,phi):
    gcd,s,_=eea(e,phi)
    if(gcd!=1):
        print('The modular inverse does not exist')
        return None
    else:
        if(s<0):
            print("s=%d. Since %d is less than 0, s = s(modr), i.e., s=%d."%(s,s,s%phi))
        elif(s>0):
            print("s=%d."%(s))
        return s%phi

def main():
    # Decide how many bits we want our primes to be
    bits = 60
    p = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
    q = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
    n = p*q
    message = 'heihei'
    print('The message is:', message)
    phi = totient(p, q)
    for i in range(1,1000):
        if(egcd(i,phi)==1):
            e=i
    d = mult_inv(e, phi)
    m = bytes_to_long(message.encode('utf-8'))
    print("p =", p)
    print("q =", q)
    print("e =", e)
    print("d =", d)
    # Encrypt bytes
    cipher = pow(m,e, n)
    print("The cipher is:", cipher)
    # Decrypt bytes
    decipher = pow(cipher,d ,n)
    plaintext = long_to_bytes(decipher)
    print("The plaintext after decrypting the cipher: ", plaintext)
    

if __name__ == "__main__":
    main()

""" p = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
q = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
 """