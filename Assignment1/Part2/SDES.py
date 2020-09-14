import numpy as np

# takes in an 8-bit block of plaintext and a 10-bit key
# produces 8-bit block of ciphertext

# Initial permutation (IP)
# A complex function fk which involves both permutation and substitusion that depends on a key input
# a simple permutation function that switches (SW) the two halves of the data
# The fk function again
# Finally a permutationfunction that is the inverse of the initial permutation (IP^-1)

key="1110001110"
cipher = "11001010"
plaintext = "10101010"

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]

IP = [2, 6, 3, 1, 4, 8, 5, 7]
IPinv = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
S0 = [[1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]]

def permutation(perm, key):
    permutated = ''
    for i in perm:
        permutated += key[i-1]
    return permutated

def generateKey(left, right):
    left1 = left[1:] + left[:1]
    rigth1 = right[1:] + right[:1]
    keyRot1 = left1 + rigth1
    left2 = left[3:] + left[:3]
    right2 = right[3:] + right[:3]
    keyRot2 = left2 + right2
    return permutation(P8, keyRot1), permutation(P8, keyRot2)

def Sbox(input, sbox):
    row = int(input[0] + input[3], 2)
    column = int(input[1] + input[2], 2)
    return bin(sbox[row][column])[2:].zfill(2)

def F(right, key):
    rightPerm = permutation(EP, right)
    XOR = bin( int(rightPerm, 2) ^ int(key, 2))[2:].zfill(8)
    print(XOR)
    left_sboxed = Sbox(XOR[:int(len(XOR)/2)], S0)
    right_sboxed = Sbox(XOR[int(len(XOR)/2):], S1)
    print(left_sboxed, right_sboxed)
    return permutation(P4, left_sboxed + right_sboxed)

def fk(bitString, key):
    leftString = bitString[:int(len(bitString)/2)]
    rightString = bitString[int(len(bitString)/2):]
    left = int(leftString, 2) ^ int(F(rightString, key), 2)
    return bin(left)[2:].zfill(4), rightString

def sdes_encrypt(bitString, key):
    P10key = permutation(P10, key)
    leftKey = P10key[:int(len(P10key)/2)]
    rightKey = P10key[int(len(P10key)/2):]
    key1, key2 = generateKey(leftKey, rightKey)
    print(key1, key2)
    bitString = permutation(IP, bitString)
    leftFK, rightFK = fk(bitString, key2)
    leftFK, rightFK = fk(rightFK + leftFK, key2)
    invPerm = permutation(IPinv, leftFK + rightFK)
    return invPerm

print(sdes_encrypt(plaintext, key))
