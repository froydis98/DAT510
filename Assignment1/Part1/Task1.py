import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

rawInput = "BQZRMQ  KLBOXE  WCCEFL  DKRYYL  BVEHIZ  NYJQEE  BDYFJO  PTLOEM  EHOMIC  UYHHTS  GKNJFG EHIMK NIHCTI HVRIHA RSMGQT RQCSXX CSWTNK PTMNSW AMXVCY WEOGSR FFUEEB DKQLQZ WRKUCO  FTPLOT  GOJZRI  XEPZSE  ISXTCT  WZRMXI  RIHALE  SPRFAE  FVYORI  HNITRG  PUHITM CFCDLA  HIBKLH  RCDIMT  WQWTOR  DJCNDY  YWMJCN  HDUWOF  DPUPNG  BANULZ  NGYPQU LEUXOV  FFDCEE  YHQUXO   YOXQUO  DDCVIR  RPJCAT  RAQVFS  AWMJCN  HTSOXQ   UODDAG BANURR REZJGD VJSXOO MSDNIT RGPUHN HRSSSF VFSINH MSGPCM ZJCSLY GEWGQT DREASV FPXEAR IMLPZW EHQGMG WSEIXE GQKPRM XIBFWL IPCHYM OTNXYV FFDCEE YHASBA  TEXCJZ VTSGBA NUDYAP IUGTLD WLKVRIHWACZG PTRYCE VNQCUP AOSPEU KPCSNG RIHLRI KUMGFC YTDQES DAHCKP BDUJPX KPYMBD IWDQEF WSEVKT CDDWLI NEPZSE OPYIW" 
rmWSInput = rawInput.replace(" ", "").strip()

EN_IC = 0.67
EN_REL_FREQ = {'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228, 'G': 0.02015,
               'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749,
               'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 'U': 0.02758,
               'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 'Z': 0.00074}

def plotDict(dict):
    lists = sorted(dict.items())
    x, y = zip(*lists)
    plt.plot(x, y)
    plt.show()

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
    return key

def splitTextinKeySize(input):
    key = findKeyLength(input)
    

splitTextinKeySize(rmWSInput)

