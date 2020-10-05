# q should be 256 bits
# p should be 1024 bits
# p-1 , has a large prime divisor q
# seeden er sharedKey fra diffiehellman

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
        seed = seed*seed % M
        b = seed % 2
        bit_output += str(b)
    return int(bit_output, 2)

def main():
    g = 2
    sharedPrime = 353
    print("The shared prime is ", sharedPrime)
    print("The generator (g) is ", g)
    alicePrivate = 143
    bobPrivate = 23
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
    CSPRNG = CSPRNG_BBS(aliceShared, 20)
    print("Stronger secret key is ", CSPRNG)


if __name__ == "__main__":
    main()
