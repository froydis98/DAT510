p = 11
q = 13
n = p*q

def totient(p, q):
    return (p-1) * (q-1)

phi = totient(p, q)

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

e = 7

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

d = modinv(e, phi)

def encrypt(message, e, n):
    return message**e % n

def decrypt(cipher, d, n):
    return cipher**d % n

message = "9"
messageBits = ' '.join(format(ord(x), 'b').zfill(8) for x in message).split(' ')

def frombits(bits):
    output = []
    for b in range(0, len(bits)):
        output.append(chr(int(bits[b], 2)))
    return ''.join(output)

frombitsmessage = frombits(messageBits)
print(int(''.join(messageBits), 2))
cipher = encrypt(int(''.join(messageBits), 2), e, n)
print(cipher)
decipher = decrypt(cipher, d, n)
print(decipher)
de = bin(decipher)[2:]
plaintext = frombits(de)
print(plaintext)
