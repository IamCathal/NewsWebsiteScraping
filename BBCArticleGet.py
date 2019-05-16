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
        html = urlopen('https://www.bbc.com/news/'+dir)
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
        html = urlopen('https://www.bbc.com/news/'+dir)
        htmlObj = BeautifulSoup(html, features="html.parser")

        articles = htmlObj.findAll("span", re.compile("(title-link__title-text)+"))
        return articles

def getArticleTopics(dir):
        html = urlopen('https://www.bbc.com/news/'+dir)
        htmlObj = BeautifulSoup(html, features="html.parser")
        articlesText = list()
        articles = htmlObj.findAll("li", "mini-info-list__item mini-info-list__item--section")
        #for elem in articles:
        #    print(elem)
        for elem in articles: 
            articlesText.append(elem.text[16:]) 
        return articlesText

def writeCSV(allArticles, allTopics, numArticles, dir):
    with open('info.csv', 'a', encoding="utf-8") as file:
        fields = ['date', 'dir', 'articleTitle','articleTopic']
        writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

        for article, topic in zip(allArticles, allTopics):
                writeObj.writerow({'date':'{}'.format(currDate), 'dir':'{}'.format(dir), 'articleTitle':'{}'.format(article.text), 'articleTopic':'{}'.format(topic)})


def getInfo(dir):

    articleCount = 0

    getTitle(dir)
    articleTitles = getArticleTitles(dir)
    articleTopics = getArticleTopics(dir)
    for article in articleTitles:
        articleCount += 1

    writeCSV(articleTitles, articleTopics, articleCount, dir)

def checkLink(url):
    try:
        html = urlopen('https://www.bbc.com/news/'+url)
    except HTTPError as err:
        return None
        exit()
    else: getInfo(url)

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
    time.sleep(5)
    
    print("Done!")

if __name__ == "__main__":
    main()


