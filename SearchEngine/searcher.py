import tokenizer
import re
import json
import os
from collections import defaultdict
import sys
import ast
import sys
import time
import math
import copy

#change the path to the finalizeP path in the indexer.py,
#they should be the same
path = "/Users/carde/alphaIndexes3"

urlMap = dict()
indexMap = dict()

timer = [0]

os.chdir(path)

print("Initualizing Dependancies")
print("Getting Index Map......")
with open(os.path.join(path,"IndexIndex.txt"), "r") as f:
    indexMap = json.loads(f.read())
print("Index Map Loaded Successfully")
print("Getting URL Map.....")
with open(os.path.join(path,"urlMap.txt"), "r") as f:
    urlMap = ast.literal_eval(f.read())
print("URL Map Loaded Successfully")
print("Dependancies Loaded\n")
print("Search -1_exit to terminate")

def search(quert):
    startTime = time.time()
    timer[0] = startTime
    queryDict = dict()
    toks = tokenizer.tokenize(quert)
    for i in list(toks.keys()):
        if i in indexMap:
            location = indexMap[i]
            f = open(os.path.join(path,"index_" + i[0] + ".txt"), "r", encoding='utf-8')
            f.seek(location, 0)
            line = f.readline()
            f.close()
            dic = line[line.index(" ")+1:]
            dic = dic.replace("\'", "\"")
            queryDict[i] = json.loads(dic)
    '''
    shortest = dict()
    for k in queryDict.keys():
        shortest[k] = len(queryDict[k])
    smallest = min(shortest.items(),key=lambda x:x[1])
    print(smallest)
    raise TypeError
    goodDocs = reduce(queryDict, smallest)
    '''
    query_tfidf = queryVect(toks, queryDict)
    urls = cosRank(queryDict, query_tfidf)
    finalize(urls)

def reduce(queryDict, smallest): # {a : {1:.8}}
    goodDocs = set()
    smK = queryDict[smallest].keys()
    for k, v in queryDict.items():
        check = v.keys()
        for doc in smK:
            if doc in check:
                goodDocs.add(doc)
    return goodDocs
            

def queryVect(query, queryDict):
    total = len(urlMap)
    for k, v in query.items():
        x = 1 + math.log(query[k])
        try: 
            df = len(queryDict[k])
        except:
            df = 1
        y = math.log(total/df)
        query[k] = x*y
    return query
        

def cosRank(queryDict, querytfidf): #cristina -1_exit
    joined = dict()
    for k, j in queryDict.items():
        '''
        for doc in goodDocs:
            try:
                top = querytfidf[k] * queryDict[k][doc]
                bot = math.sqrt(querytfidf[k]) * math.sqrt(queryDict[k][doc])
                cosSim = top/bot
                if doc in joined:
                    joined[doc] += cosSim
                else:
                    joined[doc] = cosSim
            except:
                if doc in joined:
                    joined[doc] += 0
                else:
                    joined[doc] = 0
        '''
        for doc, tfidf in j.items():
            top = querytfidf[k] * tfidf
            bot = math.sqrt(querytfidf[k]) * math.sqrt(tfidf)
            cosSim = top/bot
            if doc in joined:
                joined[doc] += cosSim
            else:
                joined[doc] = cosSim
    final = sorted(joined.items(), key=lambda item: item[1], reverse = True)
    return final[:5]

def finalize(urls):
    endTime = time.time()
    print()
    print("Search -1_exit to terminate the program")
    print()
    print("Top 5 Query results in " + str(round(endTime-timer[0],3)*1000) +" miliseconds\n")
    for i in urls:
        print(urlMap[str(i[0])] + "\n")

def main():
    query = ""
    while True:
        query = input("Search: ")
        if query == "-1_exit":
            break
        else:
            search(query)
        
if __name__ == '__main__':
    main()

