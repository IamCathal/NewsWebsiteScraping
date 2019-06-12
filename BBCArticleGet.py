import xml.etree.ElementTree as ET  
import urllib.request
import threading
import datetime
import random
import time
import csv

date = datetime.datetime.now()
currDate = '{}/{}/{}'.format(date.day,date.month,date.year)
random.seed(datetime.datetime.now())

articleURLs = ('world','uk','business','politics','health',
'education','science_and_environment','technology','entertainmant_and_arts',
'world/africa','world/asia','world/europe','world/latin_america','world/middle_east',
'world/us_and_canada','world/england','northern_ireland','scotland','wales')


def getArticles(dir):
    tree = ET.parse(source=urllib.request.urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml'))
    root = tree.getroot()
    invalidArticle = 'BBC News - '+dir
    allArticles = list()

    for elem in root.iter('title'):
        if elem.text.lower() != invalidArticle.lower():
                allArticles.append(elem.text)

    return allArticles


def writeCSV(articleList, dir):
    with open('infoXML.csv', 'a', encoding="utf-8") as file:
        fields = ['date', 'dir', 'articleTitle']
        writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

        for article in articleList:
            writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})


def scrape(dir):
    allArticles = getArticles('world')
    writeCSV(allArticles, dir)
    print("Downloaded articles from section: {}".format(dir))


def main():
    for target in articleURLs:
        scrape(target)
        waitTime = (random.random())*3
        # print("Waited {:0.2f} seconds".format(waitTime))
        time.sleep(waitTime)

   
if __name__ == '__main__':
    main()