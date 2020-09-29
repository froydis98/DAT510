import numpy as np


def calculateSecretKey(AlicePrivateKey, BobPrivateKey, prime1, prime2):
    tempKey1 = (prime1^AlicePrivateKey) % prime2
    tempKey2 = (prime1^BobPrivateKey) % prime2
    AliceSecret = (tempKey2^AlicePrivateKey) % prime2
    BobSecret = (tempKey1^BobPrivateKey) % prime2
    return AliceSecret, BobSecret


