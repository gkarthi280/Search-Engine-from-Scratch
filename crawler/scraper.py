import re
from urllib.parse import urldefrag, urlparse
import PartA
from bs4 import BeautifulSoup
from collections import defaultdict
from difflib import SequenceMatcher
import json
 
homeURL = [""]
tokens = dict() #This is a global dictionary
crawled = set()
 
def scraper(url, resp):
    #print("Scraper Started")
    homeURL.append(url)
    homeURL.pop(0)
    boot = generate_tokens(url,resp)
    if boot:
        links = extract_next_links(url, resp)
        return [link for link in links if is_valid(link)]
    else:
        return []
 
def generate_tokens(url, resp):
    if resp.status == 200:
        text = resp.raw_response.content
        soup = BeautifulSoup(text, 'html.parser')
        all_text = soup.get_text()
        all_text = re.sub(r'\n+', ' ', all_text) #easier to read
        token = PartA.tokenize(all_text)
        if token in list(tokens.values()):
            # print("Here")
            return False
        else:
            crawled.add(url)
            tokens[url] = token
            return True
        
        
 
def extract_next_links(url, resp):
    links = []
    #print(homeURL)
    if resp.status == 200:
        text = resp.raw_response.content
        soup = BeautifulSoup(text, 'html.parser')
        for link in soup.find_all('a'):
            temp = link.get('href')
            pure_url, trash = urldefrag(temp)
            links.append(pure_url)
            links = list(set(links))
        return links
    return list()
 
def is_valid(url):
    try:
        parsed = urlparse(url)
        homeParsed = urlparse(homeURL[0])
        if url in crawled:
            return False
        if parsed.scheme not in set(["http", "https"]):
            return False
        val = False
        for link in {".ics.uci.edu",".cs.uci.edu",".informatics.uci.edu",".stat.uci.edu"}:
            if link in parsed.hostname:
                val = True
        if val:
            similar_index = SequenceMatcher(None, homeURL[0], url).ratio()
            if (similar_index) > 0.95:
                val = False
            if "?" in url:
                val = False
            if re.search(r"([0-9]{4}|[0-9]{2})-([0-9]{2})-([0-9]{2})",url):
                val = False
            if re.search(r"([0-9]{4}|[0-9]{2})-([0-9]{2})",url):
                val = False
        if not val:
            return val
        return not re.match(
         r".*\.(css|js|bmp|gif|jpe?g|ico"
         + r"|png|tiff?|mid|mp2|mp3|mp4"
         + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
         + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
         + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
         + r"|epub|dll|cnf|tgz|sha1"
         + r"|thmx|mso|arff|rtf|jar|csv"
         + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    except TypeError:
        return False
 
def recorder():
    file = open("Analytics.txt", "w")
    #1st Doc Req
    file.write("Number of unique pages: " + str(len(tokens)) + "\n\n")
    #2nd Doc Req
    longURL = longestPage()
    file.write("Page with the most words: " + longURL + "\n\n")
    #3rd Doc Req
    rank = 1
    topWords = top50()
    file.write("Word Rankings: \n")
    for i in topWords:
        file.write(str(rank) + ": " + str(i[0])+ "\n")
        rank += 1
    #4th Doc Req
    subs = subDomains()
    file.write("\n\n")
    file.write("SubDomains in ics.uci.edu: " + str(len(subs)) + "\n")
    file.write("SubDomain in ics.uci.edu count: \n")
    for i in subs:
        file.write(str(i[0]) + ", " + str(i[1]) + "\n")
    file.close()
    
    
def longestPage():
    count = 0
    url = ''
    for i in tokens:
        counter = 0
        for j in tokens[i]:
            counter += tokens[i][j]
        if counter > count:
            count = counter
            url = i
    return url
 
def top50():
    count = 0
    newDict = dict()
    for i in tokens:
        for j in tokens[i]:
            if j not in newDict.keys():
                newDict[j] = tokens[i][j]
            else:
                newDict[j] += tokens[i][j]
    final = sorted(newDict.items(), key=lambda item: item[1], reverse = True)
    return final[:50]
 
def subDomains():
    myDict = defaultdict(int)
    for url in tokens:
        parsed = urlparse(url)
        if ".ics.uci.edu" in url:
            myDict[parsed.netloc] += 1;
    return sorted(myDict.items(), key=lambda x: x[0])
