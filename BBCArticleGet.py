import xml.etree.ElementTree as ET  
from urllib.error import HTTPError
import urllib.request
import threading
import datetime
import random
import time
import csv
import re

date = datetime.datetime.now()
currDate = '{}/{}/{}'.format(date.day,date.month,date.year)
random.seed(datetime.datetime.now())

articleURLs = ('world','uk','business','politics','health',
'education','science_and_environment','technology','entertainment_and_arts',
'world/africa','world/asia','world/europe','world/latin_america','world/middle_east',
'world/us_and_canada','england','northern_ireland','scotland','wales')


def getArticles(dir):
    try:
        tree = ET.parse(source=urllib.request.urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml'))
    except HTTPError as err:
        # print(err)
        return None
    except ET.ParseError as err:
         return None
    else:
        root = tree.getroot()
        allArticles = list()
        for elem in root.iter('title'):
            if not re.match('^(BBC News)+', elem.text):
                    allArticles.append(elem.text)

        return allArticles


def writeCSV(articleList, dir, invalid):
    if invalid:
        with open('errorLog.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})
    else:
        with open('infoXML.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})


def scrape(dir):
    allArticles = getArticles(dir)
    if allArticles != None:
        writeCSV(allArticles, dir, 0)
        print('Downloaded articles from section: {}'.format(dir))
    else:
        badScrapeMsg = 'Error could not scrape from section: {}'.format(dir)
        badScrape = list()
        badScrape.append(badScrapeMsg)
        writeCSV(badScrape, dir, 1)
        print('############ Failed to download articles from section: {} ############ '.format(dir))



def main():
    for target in articleURLs:
        scrape(target)
        waitTime = (random.random())*3
        # print("Waited {:0.2f} seconds".format(waitTime))
        time.sleep(waitTime)

   
if __name__ == '__main__':
    main()