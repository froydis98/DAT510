import numpy as np

# takes in an 8-bit block of plaintext and a 10-bit key
# produces 8-bit block of ciphertext

# Initial permutation (IP)
# A complex function fk which involves both permutation and substitusion that depends on a key input
# a simple permutation function that switches (SW) the two halves of the data
# The fk function again
# Finally a permutationfunction that is the inverse of the initial permutation (IP^-1)

RawKey = ['0000000000', '0000011111', '0010011111', '0010011111', '1111111111', '0000011111', '1000101110', '1000101110']
PlainText = [00000000, 11111111, 11111100, 10100101]
CipherText = [0, 0, 0, ]


def initialPermutation()