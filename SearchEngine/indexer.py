from bs4 import BeautifulSoup
import tokenizer
import re
import json
import os
from collections import defaultdict
import sys
import ast
import sys
import math



index = dict()
urlMap = dict()
#change the paths to create your index
devpath = "/Users/carde/Downloads/developer/DEV"
indexpath = "/Users/carde/indexes"
finalizeP = "/Users/carde/alphaIndexes3"
finalpath = "/Users/carde/alphaIndexes2"

def findFiles():
    indexesLoaded = 0
    docID = 0
    os.chdir(devpath)
    for folder in os.listdir(os.getcwd()):
        print(folder)
        os.chdir(devpath + "/" +folder)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".json"):
                processFile(file, docID)
                docID += 1
            if sys.getsizeof(index) >= 100000:
                offload(indexesLoaded)
                indexesLoaded += 1
    if sys.getsizeof(index) != 0:
        offload(indexesLoaded)
    createIndexFiles()
        

def processFile(file, ID):
    f = open(file,"r")
    stuff = json.load(f)
    f.close()
    urlMap[ID] = stuff["url"]
    soup = BeautifulSoup(stuff["content"],'html.parser')
    header = soup.find_all(re.compile(r"^h[1-6]$"))
    h_words = []
    for i in header:
        ts = i.text.strip()
        kns = tokenizer.tokenize(ts)
        h_words += kns.keys()
    strong = soup.find_all("b")
    s_words = []
    for i in strong:
        ts = i.text.strip()
        kns = tokenizer.tokenize(ts)
        s_words += kns.keys()
    try:
        title = soup.title.string
        t_words = list(tokenizer.tokenize(title).keys())
    except:
        t_words = []
    text = soup.getText()
    tokens = tokenizer.tokenize(text)
    for token in tokens:
        if token in index:
            if token in t_words:
                index[token][ID] = 1 + math.log(tokens[token]+3)
            elif token in h_words:
                index[token][ID] = 1 + math.log(tokens[token]+2)
            elif token in s_words:
                index[token][ID] = 1 + math.log(tokens[token]+1)
            else:
                index[token][ID] = 1 + math.log(tokens[token])
        else:
            if token in t_words:
                index[token] = {ID : 1 + math.log(tokens[token]+3)}
            elif token in h_words:
                index[token] = {ID : 1 + math.log(tokens[token]+2)}
            elif token in s_words:
                index[token] = {ID : 1 + math.log(tokens[token]+1)}
            else:
                index[token] = {ID : 1 + math.log(tokens[token])}
    
def offload(loaded):
    filename = "index" + str(loaded) + ".txt"
    with open(os.path.join(indexpath,filename), "w") as f:
        f.write(json.dumps(index))
    index.clear()


def createIndexFiles():
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "0","1","2","3","4","5","6","7","8","9"]
    for letter in alpha:
        print(letter)
        lIndex = dict()
        os.chdir(indexpath)
        for file in os.listdir(os.getcwd()):
            filename = "index_" + letter + ".txt"
            f = open(os.path.join(indexpath,file), "r")
            mess = ast.literal_eval(f.read())
            f.close()
            content = 0
            used = []
            for word, dic in mess.items():
                if word[0] == letter:
                    if word in lIndex:
                        lIndex[word].update(mess[word])
                    else:
                        lIndex[word] = mess[word]
            #for word in used:
                #del mess[word]
            used = []
            f = open(os.path.join(indexpath,file), "w")
            f.write(json.dumps(mess))
            f.close()
            mess.clear()
        t = open(os.path.join(finalpath,filename), "w")
        t.write(json.dumps(lIndex))
        t.close()
        lIndex.clear()

def finalize():
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "0","1","2","3","4","5","6","7","8","9"]
    filename = "urlMap.txt"
    with open(os.path.join(finalizeP,filename), "w") as e:
        e.write(json.dumps(urlMap))
        total = len(urlMap)
        urlMap.clear()
    for letter in alpha:
        print(letter)
        lIndex = dict()
        os.chdir(finalpath)
        filename = "index_" + letter + ".txt"
        l = open(os.path.join(finalizeP,filename), "w", encoding='utf-8')
        f = open(os.path.join(finalpath,filename), "r")
        mess = ast.literal_eval(f.read()) #a
        f.close()
        mess = calc_tfidf(mess, total)
        string = ""
        for word, dic in mess.items():
            if word[0] == letter:
                string = word + " "
                string = string + str(dic) + "\n"
                l.write(string)
        l.close()
            
def createHelpers():
    indexIndex = defaultdict(int)
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
             "0","1","2","3","4","5","6","7","8","9"]
    for letter in alpha:
        print(letter)
        lIndex = dict()
        os.chdir(finalizeP)
        filename = "index_" + letter + ".txt"
        l = open(os.path.join(finalizeP,filename), "r", encoding='utf-8')
        pos = 0
        line = l.readline()
        while line:
            indexIndex[line[:line.index(" ")]] = pos
            pos = l.tell()
            line = l.readline()
    t = open(os.path.join(finalizeP,"IndexIndex.txt"), "w", encoding='utf-8')
    t.write(json.dumps(indexIndex))
    t.close()

def calc_tfidf(mess, total):
    for k, v in mess.items(): # {"at" {1: x, 2:y}}
        df = len(v)
        for doc, tf in v.items():
            mess[k][doc] = tf*math.log(total/df)
    return mess
        

def main():
    findFiles()
    finalize()
    createHelpers()
        
if __name__ == '__main__':
    main()
