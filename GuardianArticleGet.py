import xml.etree.ElementTree as ET
from urllib.error import HTTPError
import urllib.request
import datetime
import random
import time
import csv
import re

date = datetime.datetime.now()
currDate = '{}/{}/{}'.format(date.day,date.month,date.year)
random.seed(datetime.datetime.now())


def getArticles(searchType):
    try:
        tree = ET.parse(source=urllib.request.urlopen('https://www.theguardian.com/sitemaps/news.xml'))
    except HTTPError as err:
        print(err)
        return None
    except ET.ParseError as err:
        print(err)
        return None
    else:
        root = tree.getroot()
        i = 0

        if searchType == 'titles':
            allTitles = list()
            for elem in root.iter('{http://www.google.com/schemas/sitemap-news/0.9}title'):
                allTitles.append(elem.text.strip())
                i += 1
            print('{} article titles scraped'.format(i))
            return allTitles

        else:
            allKeywords = list()
            tempKeywords = list()
            keywordString = ''

            for elem in root.iter('{http://www.google.com/schemas/sitemap-news/0.9}keywords'):
                keywordString = elem.text
                tempKeywords = keywordString.split(',')
                allKeywords.append(tempKeywords)
                i += 1
            print('{} article keyword lists scraped'.format(i))
            return allKeywords

    
def getKeywords():
    try:
        tree = ET.parse('guardian.xml')
    except HTTPError as err:
        print(err)
        return None
    else:
        root = tree.getroot()
        
        print(root)


def writeCSV(allTitles, allKeywords, date):
    with open('guardianInfo.csv', 'w', encoding='utf-8') as file:
        i = 0
        fields = ['date','keywordsArr', 'articleTitle']
        writeObj = csv.DictWriter(file, fieldnames=fields, delimiter=',',lineterminator='\n')

        for title, keywords in zip(allTitles, allKeywords):
            writeObj.writerow({'date':'{}'.format(currDate),'keywordsArr':'{}'.format(keywords),'articleTitle':'{}'.format(title)})
            i += 1

        print('{} lines written'.format(i))


def scrape():
    titlesList = getArticles('titles')
    keywordsList = getArticles('keywords')

    if titlesList and keywordsList != None:
        writeCSV(titlesList, keywordsList, currDate)


def main():
    scrape()
    
  
if __name__ == '__main__':
    main()

