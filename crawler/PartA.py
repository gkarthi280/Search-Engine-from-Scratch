import re
import sys
import builtins

stopWords = {"a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"}

def tokenize(text):
    tokens = text.lower()
    tokens = re.findall(r"\b[a-z0-9']{3,}", tokens)  
    tokens = computeWordFreq(tokens)
    return tokens

def computeWordFreq(token):
    feqDict = dict() #O(1)
    for i in token: #O(N)
        if i not in stopWords:
            tok = i
            if tok in feqDict: #O(N)
                feqDict[i] += 1 #O(1)
            else:
                key = i
                feqDict[key] = 1 #O(1)
    return feqDict

def WordFreqPrint(frequencies):
    string = "" #O(1)
    sortLst = sorted(frequencies.items(), key=lambda x: x[1], reverse=True) #O(N)
    for i in sortLst: #O(N)
        string += i[0] + " = " 
        string += str(i[1])
        string += "\n"
    builtins.print(string)
    
'''
    def main():
    args = sys.argv[1:] #O(N)
    for i in args: #O(N)
        print(computeWordFrequencies(tokenize(i)))
        
if __name__ == '__main__':
    main()

'''  
