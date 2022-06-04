import re
import sys
import time

def tokenSet(fle):
    #Test for Non English Characters and 's
    '''
    Runtime Complexity
    '''
    t1 = time.time()
    tokSet = set()
    try:
        file = open(fle,"r", errors="ignore")
        flines = file.readlines()
        first = open("fst.txt",'w')
        last = open("lst.txt",'w')
        first.write("".join(flines[0:int(len(flines)/2)+1]))
        last.write("".join(flines[int((len(flines)/2))]))
        first.close()
        last.close()
        first = open("fst.txt","r")
        last = open("lst.txt",'r')
        for file in (first,last):
            for line in file:
                print(line)
                tokens = line.lower().split()
                for token in tokens:
                    token = re.sub(r"[^a-zA-Z0-9']"," ",token)
                    tokSet.add(token.strip())
            file.close()
    except FileNotFoundError:
        print("File Not Found")
    t2 = time.time()
    runtimes.append((t2-t1))
    return tokSet
            
def computeCommons(set1, set2):
    '''
    Runtime Complexity
    '''
    t1 = time.time()
    if len(set1) < len(set2):
        sharedSet = set1.intersection(set2)
    else:
        sharedSet = set2.intersection(set1)
    t2 = time.time()
    runtimes.append((t2-t1))
    return len(sharedSet)

def main():
    '''
    Runtime Complexity
    '''
    args = sys.argv[1:]
    i = 0
    while i < len(args)-1:
        set1 = tokenSet(args[i])
        set2 = tokenSet(args[i+1])
        print(computeCommons(set1, set2))
        i = i + 2
        
runtimes = []
main()
print(runtimes)
