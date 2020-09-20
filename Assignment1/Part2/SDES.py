import re

# takes in an 8-bit block of plaintext and a 10-bit key
# produces 8-bit block of ciphertext

# Initial permutation (IP)
# A complex function fk which involves both permutation and substitusion that depends on a key input
# a simple permutation function that switches (SW) the two halves of the data
# The fk function again
# Finally a permutationfunction that is the inverse of the initial permutation (IP^-1)

message1='010001110000000101000000110011011100101100000001011101000000000101101110010101110101011101101110010001110000000101000111101110100100111110001000010001110110111001001100101011111001011101101110011011101011101001001111101011110000100101001010100010000100111111001101100101110100111100110010000000010101011101101110100100000100111110101111010001111010111101110100011101000000000101001100000000010110111010111010100010000100011101101110010011001010111110010111000000011000100010010000'
message2='000000011010011100110010110001100110010010100111110101111010011110011100011101000111010010011100000000011010011100000001100110011010000111011010000000011001110011101111011111100010010010011100100111001001100110100001011111101010000010110011110110101010000111000110001001001010000100100011101001110111010010011100010000011010000101111110000000010111111011010111110101111010011111101111101001111001110010011001110110100000000110011100111011110111111000100100101001111101101001000001'
key="1000101110"
cipher = "11000010"
plaintext = "10100101"

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
    left_sboxed = Sbox(XOR[:int(len(XOR)/2)], S0)
    right_sboxed = Sbox(XOR[int(len(XOR)/2):], S1)
    return permutation(P4, left_sboxed + right_sboxed)

def fk(bitString, key):
    leftString = bitString[:int(len(bitString)/2)]
    rightString = bitString[int(len(bitString)/2):]
    left = int(leftString, 2) ^ int(F(rightString, key), 2)
    return bin(left)[2:].zfill(4), rightString

def SDES(bitString, key, decrypt=False):
    P10key = permutation(P10, key)
    leftKey = P10key[:int(len(P10key)/2)]
    rightKey = P10key[int(len(P10key)/2):]
    key1, key2 = generateKey(leftKey, rightKey)
    if decrypt:
        key2, key1 = key1, key2
    bitStringPerm = permutation(IP, bitString)
    leftFK, rightFK = fk(bitStringPerm, key1)
    leftFK, rightFK = fk(rightFK + leftFK, key2)
    invPerm = permutation(IPinv, leftFK + rightFK)
    return invPerm

def tripleSDES(bitString, rawKey1, rawKey2, decrypt=False):
    firstRound = SDES(bitString, rawKey1, decrypt)
    secondRound = SDES(firstRound, rawKey2, not decrypt)
    thirdRound = SDES(secondRound, rawKey1, decrypt)
    return thirdRound

def frombits(bits):
    output = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        output.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(output)

def bruteForceSDES(message):
    rounds = len(message)/8
    pattern = re.compile("^[a-zA-Z]+$")
    for i in range(2**10):   
        answer =''
        tryKey = bin(i).replace('0b', '').zfill(10)
        start = 0
        for j in range(int(rounds)):
            decrypted = SDES(message[start:start+8], tryKey, True)
            answer += frombits(decrypted)
            if not pattern.match(answer):
                break
            start += 8
        if pattern.match(answer):
            return answer

def bruteForceTripleSDES(message):
    rounds = len(message)/8
    pattern = re.compile("^[a-zA-Z]+$")
    for i in range(2**10):   
        tryKey1 = bin(i).replace('0b', '').zfill(10)
        for j in range (2**10):  
            answer = ''
            start = 0
            tryKey2 = bin(j).replace('0b', '').zfill(10)
            for k in range(int(rounds)):
                decrypted = tripleSDES(message[start:start+8], tryKey1, tryKey2, True)
                answer += frombits(decrypted)
                if not pattern.match(answer):
                    break
                start += 8
            if pattern.match(answer):
                return answer

