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

articleURLs = ('edition','edition_world','edition_africa','edition_americas',
'edition_asia','edition_europe','edition_meast','edition_us','money_news_international',
'edition_technology','edition_space','edition_entertainment','edition_sport',
'edition_football','edition_golf','edition_motorsport','edition_tennis')


def getArticles(dir):
    try:
        tree = ET.parse(source=urllib.request.urlopen('http://rss.cnn.com/rss/'+dir+'.rss'))
    except HTTPError as err:
        # print(err)
        return None
    except ET.ParseError as err:
         return None
    else:
        root = tree.getroot()
        allArticles = list()
        for elem in root.iter('title'):
            allArticles.append(elem.text)

        return allArticles
        
    	
def writeCSV(articleList, dir, invalid):
    if invalid:
        with open('CNNerrorLog.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})
    else:
        with open('CNNinfoXML.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir[8:]),'articleTitle':'{}'.format(article)})


def scrape(dir):
    allArticles = getArticles(dir)
    if allArticles != None:
        writeCSV(allArticles, dir, 0)
        print('Downloaded articles from section: {}'.format(dir[8:]))
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