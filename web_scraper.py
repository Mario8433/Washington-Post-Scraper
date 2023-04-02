from requests import get
from itertools import count
from bs4 import BeautifulSoup
import os, sys

def main():
    res = request(sys.argv[1])
    content = scrape(res)
    path = save(content)
    print('\nDone! Scraped content has generated at ' + path)


def request(url): # Request URL from the the terminal
    
    print('\nLoading...')
    try:
        res = get(url)
        res.encoding = 'utf-8'
        return res
    except:
        print('\nLink is inaccessible.')
        sys.exit()


def scrape(res): # Scrape the webpage and return the reorganized text
    
    content = ''
    
    soup = BeautifulSoup(res.content, 'html.parser')
    text = soup.find_all(attrs={'data-el':'text'})
    
    for i in text:
        content += i.get_text() + '\n\n'
    if content == '':
        print('\nThe webpage content is inaccessible. This may because:\n1. The news service requires subscription\n2. The news webpage does not use a conventional data tag.\n3. This is not a news webpage.\nPlease try other scraper service.')
        sys.exit()
    
    content = write_head(soup) + content
    return content

def save(content): # Write the reorganized content as a .txt file
    path = filename('content')
    with open(filename('content'),'w',encoding='utf-8') as f:
        f.write(content)
    return path

def write_head(soup): # Collect headline, author, and time information
    headline = soup.find(attrs={"data-qa":"headline-text"})
    author = soup.find(attrs={"data-qa":"author-name"})
    time = soup.find(attrs={"data-testid":"display-date"})
    
    List = error_check([headline,author,time])
    content = 'Title: ' + List[0] + '\n\nAuthor: ' + List[1] + '\n\nDate: ' + List[2] + '\n\n\n\n'
    return content

def filename(filename): # Generate a filename. If there is a file already, add a number behind the name.
    c = 0
    path = filename + '.txt' 
    for i in count():
        while os.path.exists(path):
            c += 1
            path = filename + str(c) + '.txt'
        break
    return path

def error_check(List): # Replace the invalid information with the placeholder.
    for i in range(len(List)):
        try:
            List[i] = List[i].get_text()
        except:
            List[i] = 'Unknown'
    return List
            
    

main()