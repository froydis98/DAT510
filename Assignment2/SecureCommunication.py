from SDES import SDES, frombits

# Creates the public key, which is the first part of diffie-hellman key exchange
def publicKey(privateKey, g, prime):
    return g**privateKey % prime

# Uses the public key to the other part and your private key to create the shared key
# The shared key is a secret key, which only Alice and Bob will know.
def sharedKey(publicKey, privateKey, prime):
    return publicKey**privateKey % prime

# Blum blum shub implementation
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

# Part 1
def main():
    # the generator g is pre defined as 2
    g = 2
    # The shared prime is a Sophie Germain prime
    sharedPrime = 683
    print("The shared prime is ", sharedPrime)
    print("The generator (g) is ", g)
    # Alice and Bob's private keys which is secret.
    alicePrivate = 217
    bobPrivate = 131
    print("Alice's private key is ", alicePrivate)
    print("Bob's private key is ", bobPrivate)
    # Creates the public key which can be sent over to the other part.
    alicePublic = publicKey(alicePrivate, g, sharedPrime)
    bobPublic = publicKey(bobPrivate, g, sharedPrime)
    print("Alice's public key is ", alicePublic)
    print("Bob's public key is ", bobPublic)
    # Creates the shared secret key. Alice and Bob should have the same number
    # If they not have the same number they do not use the same prime and generator
    aliceShared = sharedKey(bobPublic, alicePrivate, sharedPrime)
    bobShared = sharedKey(alicePublic, bobPrivate, sharedPrime)
    print("Alice's shared key is ", aliceShared)
    print("Bob's shared key is ", bobShared)
    # Uses the pseudo-random number generator Blum Blum Shub to strengthen the key
    # We choose how many bits long we want the key to be. In this case I chose 10
    secretKeyBit = CSPRNG_BBS(aliceShared, 10)
    secretKey = int(secretKeyBit, 2)
    print("Stronger secret key is ", secretKey)
    yesOrNo = input("Do you want to send a predefined message? y/n: ")
    if yesOrNo == 'y' or yesOrNo == 'Y' or yesOrNo == 'yes':
        message = "This is a super secret message"
    else:
        message = input("Write your own message to Bob: ")
    print("Alices message is: ", message)
    # Converts the message into bits
    messageBits = ' '.join(format(ord(x), 'b').zfill(8) for x in message).split(' ')
    encrypted = []
    # Encrypts the message, by using SDES from Assignment 1.
    # The key used in the encryption is the secret key we got from diffie-hellman and BBS.
    for i in range(0, len(message)):
        encrypted.append(SDES(messageBits[i], secretKeyBit))
    print("Encrypted text from Alice to Bob: ", encrypted)
    decrypted = ''
    # Decrypts the message using the same key
    for i in range (0, len(encrypted)):
        decrypted += frombits(SDES(encrypted[i], secretKeyBit, True))
    print("The message that Bob gets is: ", decrypted)


if __name__ == "__main__":
    main()
