from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import datetime
import time
import csv
import re

date = datetime.datetime.now()
currDate = '{}/{}/{}'.format(date.day,date.month,date.year)

def getTitle(dir):
    try:
        html = urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml')
    except HTTPError as err:
        print(err)
        return None
    try:
        htmlObj = BeautifulSoup(html, features="html.parser")
    except AttributeError as err:
        return None
    else:
        title = htmlObj.title.text
        print('Downloaded articles from '+title)


def getArticleTitles(dir):
        html = urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml')
        htmlObj = BeautifulSoup(html, features="html.parser")

        articles = list()
        articles = htmlObj.findAll("li")
        return articles
      

def writeCSV(allArticles, dir):
    with open('infocheck.csv', 'a', encoding="utf-8") as file:
        fields = ['date', 'dir', 'articleTitle']
        writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

        for article in allArticles:
            writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})


def getInfo(dir):

    getTitle(dir)
    
    articleTitles = getArticleTitles(dir)

    writeCSV(articleTitles, dir)


def main():
    getInfo('england')
    time.sleep(5)
    getInfo('northern_ireland')
    time.sleep(5)
    getInfo('scotland')
    time.sleep(5)
    getInfo('wales')
    time.sleep(5)
    getInfo('politics')
    time.sleep(5)
    # Brexit
    getInfo('politics/uk_leaves_the_eu')
    time.sleep(5)
    getInfo('technology')
    time.sleep(5)
    # Global Trade
    getInfo('business-38507481')
    time.sleep(5)
    # Connected World
    getInfo('business-45489065')
    
    print("Done!")

if __name__ == "__main__":
    main()


