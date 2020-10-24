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

def encrypt(message, e, n):
    return message**e % n

def decrypt(cipher, d, n):
    return cipher**d % n

def main():
    p = 11
    q = 13
    n = p*q
    phi, e, d = generateKeys(p, q, n)
    message = 9
    cipher = encrypt(message, e, n)
    decrypted = decrypt(cipher, d, n)
    print(decrypted)

if __name__ == "__main__":
    main()
    