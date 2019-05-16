from bs4 import BeautifulSoup
from urllib.request import urlopen
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
        print(title)

def getArticleTitles(dir):
        html = urlopen('https://www.bbc.com/news/'+dir)
        htmlObj = BeautifulSoup(html, features="html.parser")

        articles = htmlObj.findAll("span", "title-link__title-text")
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
    with open('info.csv', 'a') as file:
        fields = ['date', 'dir', 'articleTitle','articleTopic']
        writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

        for article, topic in zip(allArticles, allTopics):
                writeObj.writerow({'date':'{}'.format(currDate), 'dir':'{}'.format(dir), 'articleTitle':'{}'.format(article.text), 'articleTopic':'{}'.format(topic)})


def getInfo(dir):

    getTitle(dir)

    articleTitles = getArticleTitles(dir)
    articleTopics = getArticleTopics(dir)
    articleCount = 0
    for article in articleTitles:
        articleCount += 1

    writeCSV(articleTitles, articleTopics, articleCount, dir)

def checkLink(url):
    try:
        html = urlopen('https://www.bbc.com/news/'+url)
    except HTTPerror as err:
        return None
    else: getInfo(url)


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
getInfo('politics/uk_leaves_the_eu')
time.sleep(5)
getInfo('technology')
time.sleep(5)
print("Done!")

