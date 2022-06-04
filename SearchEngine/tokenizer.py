import re
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(text):
    lst = [] #O(1)
    try:
        tokens = text.lower()
        tokens = nltk.word_tokenize(tokens)
        lst += tokens 
    except FileNotFoundError:
        return lst
    else:
        return computeWordFreq(tokens) #Change this to change Index Creation

def computeWordFreq(token):
    feqDict = dict()
    for i in token:
        if i[0] in "abcdefghijklmnopqrstuvwxyz0123456789":
            tok = stemmer.stem(i)
            if tok in feqDict: 
                feqDict[tok] += 1 
            else:
                feqDict[tok] = 1 
    return feqDict

def computeWordPositions(tokens):
    positionDict = {}
    i = 0
    while i < len(tokens):
        if tokens[i][0] in "abcdefghijklmnopqrstuvwxyz":
            tok = stemmer.stem(tokens[i])
            if tok in positionDict:
                positionDict[tok].append(i)
            else:
                positionDict[tok] = [i]
        i += 1
    return positionDict



    
