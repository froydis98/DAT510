from SDES import SDES, frombits

def publicKey(privateKey, g, prime):
    return g**privateKey % prime

def sharedKey(publicKey, privateKey, prime):
    return publicKey**privateKey % prime

def CSPRNG_BBS(seed, size):
    p = 7
    q = 11
    M = p*q
    bit_output = ""
    for _ in range(size):
        if seed < 2:
            return "The seed can't be 0 or 1"
        factorials = []
        for i in range (1, seed + 1 , 1):
            if seed % (i) == 0:
                if i == p or i == q:
                    return "p and q can not be factors of the seed"
        seed = (seed**2) % M
        b = seed % 2
        bit_output += str(b)
    return bit_output

def main():
    g = 2
    sharedPrime = 683
    print("The shared prime is ", sharedPrime)
    print("The generator (g) is ", g)
    alicePrivate = 217
    bobPrivate = 131
    print("Alice's private key is ", alicePrivate)
    print("Bob's private key is ", bobPrivate)
    alicePublic = publicKey(alicePrivate, g, sharedPrime)
    bobPublic = publicKey(bobPrivate, g, sharedPrime)
    print("Alice's public key is ", alicePublic)
    print("Bob's public key is ", bobPublic)
    aliceShared = sharedKey(bobPublic, alicePrivate, sharedPrime)
    bobShared = sharedKey(alicePublic, bobPrivate, sharedPrime)
    print("Alice's shared key is ", aliceShared)
    print("Bob's shared key is ", bobShared)
    secretKeyBit = CSPRNG_BBS(aliceShared, 10)
    secretKey = int(secretKeyBit, 2)
    print("Stronger secret key is ", secretKey)
    message = "Supermegahemmelig tekst"
    print("Alices message is: ", message)
    messageBits = ' '.join(format(ord(x), 'b').zfill(8) for x in message).split(' ')
    encrypted = []
    for i in range(0, len(message)):
        encrypted.append(SDES(messageBits[i], secretKeyBit))
    print("Encrypted text from Alice to Bob: ", encrypted)
    decrypted = ''
    for i in range (0, len(encrypted)):
        decrypted += frombits(SDES(encrypted[i], secretKeyBit, True))
    print("The message that Bob gets is: ", decrypted)


if __name__ == "__main__":
    main()
