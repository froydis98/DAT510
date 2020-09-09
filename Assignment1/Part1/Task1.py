import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

rawInput = "BQZRMQ  KLBOXE  WCCEFL  DKRYYL  BVEHIZ  NYJQEE  BDYFJO  PTLOEM  EHOMIC  UYHHTS  GKNJFG EHIMK NIHCTI HVRIHA RSMGQT RQCSXX CSWTNK PTMNSW AMXVCY WEOGSR FFUEEB DKQLQZ WRKUCO  FTPLOT  GOJZRI  XEPZSE  ISXTCT  WZRMXI  RIHALE  SPRFAE  FVYORI  HNITRG  PUHITM CFCDLA  HIBKLH  RCDIMT  WQWTOR  DJCNDY  YWMJCN  HDUWOF  DPUPNG  BANULZ  NGYPQU LEUXOV  FFDCEE  YHQUXO   YOXQUO  DDCVIR  RPJCAT  RAQVFS  AWMJCN  HTSOXQ   UODDAG BANURR REZJGD VJSXOO MSDNIT RGPUHN HRSSSF VFSINH MSGPCM ZJCSLY GEWGQT DREASV FPXEAR IMLPZW EHQGMG WSEIXE GQKPRM XIBFWL IPCHYM OTNXYV FFDCEE YHASBA  TEXCJZ VTSGBA NUDYAP IUGTLD WLKVRIHWACZG PTRYCE VNQCUP AOSPEU KPCSNG RIHLRI KUMGFC YTDQES DAHCKP BDUJPX KPYMBD IWDQEF WSEVKT CDDWLI NEPZSE OPYIW" 
rmWSInput = rawInput.replace(" ", "").strip()

EN_IC = 0.67
englishFreq = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043,
    'E': 0.127, 'F': 0.022, 'G': 0.020, 'H': 0.061,
    'I': 0.070, 'J': 0.002, 'K': 0.008, 'L': 0.040,
    'M': 0.024, 'N': 0.067, 'O': 0.075, 'P': 0.019,
    'Q': 0.001, 'R': 0.060, 'S': 0.063, 'T': 0.091,
    'U': 0.028, 'V': 0.010, 'W': 0.023, 'X': 0.001,
    'Y': 0.020, 'Z': 0.001}

def countLetters(input):
    charFrequency = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 
            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 
            'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for i in input:
        if i in charFrequency:
            charFrequency[i] += 1
        else:
            charFrequency[i] = 1
    return charFrequency

# https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
def findIndexOfDuplicates(input, sub):
    start = -1
    indexes = []
    while True:
        try:
            index = input.index(sub, start + 1)
        except ValueError:
            break
        else:
            indexes.append(index)
            start = index
    return indexes

def findFactorialsOnWordIndex(input, index):
    factorials = []
    wordsIndex = findIndexOfDuplicates(input, index)
    for i in range(0, len(wordsIndex)):
        if i > 0:
            indexDiff = wordsIndex[i] - wordsIndex[i-1]
    for i in range (1, indexDiff + 1 , 1):
        if indexDiff % (i) == 0:
            if i <= 10 and i > 1:
                factorials.append(i)
    return factorials

# https://cs.stackexchange.com/questions/79182/im-looking-for-an-algorithm-to-find-unknown-patterns-in-a-string
def findKeyLength(input):
    wordsFrequently = {}
    wordsIndex = []
    for i in range(3, int(len(input)/2)):
        for j in range(0, len(input)-i):
            sub = input[j:j+i]
            count = input.count(sub)
            if count >= 2 and sub not in wordsFrequently:
                wordsFrequently[sub] = count
                wordsIndex.append(findFactorialsOnWordIndex(input, sub))
    possibleKeyLengths = Counter(np.concatenate(wordsIndex))
    occurances = 0
    key = 0
    dict_keys = list(possibleKeyLengths.keys())
    dict_values = list(possibleKeyLengths.values())
    for i in range(0, len(dict_values)):
        if dict_values[i] >= occurances and dict_keys[i] > key:
            occurances = dict_values[i]
            key = dict_keys[i]
    return int(key)

# chi-square statistics
def chiSquare(letterOccurance, keyLength, inputLength):
    freqVal = list(englishFreq.values())
    sum = []
    for i in range(0, keyLength):  
        temp = []
        values = list(letterOccurance[i].values())
        for j in range(26):
            result = 0
            for k in range(26):
                result += ((values[((j+k)%26)] - (freqVal[k]*inputLength))**2)/(freqVal[k]*inputLength)
            temp.append(int(result))
        sum += [temp]
    indexSmallest = []
    for i in range(0, len(sum)):
        smallest = min(sum[i])
        indexSmallest.append(sum[i].index(smallest))
    return indexSmallest

def findKey(input):
    keyLength = findKeyLength(input)
    keyLengthSortedText = []
    letterOccurance = []
    for i in range(0,len(input)):
        if len(keyLengthSortedText) < keyLength:
            keyLengthSortedText.append(input[i])
        else: 
            keyLengthSortedText[i % keyLength] += input[i]
    for i in range(0, keyLength):
        letterOccurance.append(countLetters(keyLengthSortedText[i]))
    indexes = chiSquare(letterOccurance, keyLength, len(input))
    key = []
    alphabet = list(englishFreq.keys())
    for i in range(len(indexes)):
        key.append(alphabet[indexes[i]])
    return key



print(findKey(rmWSInput))