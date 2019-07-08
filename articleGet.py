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

# Directories for the BBC news webpages I'm interested in
BBCArticleURLs = ('world','uk','business','politics','health',
'education','science_and_environment','technology','entertainment_and_arts',
'world/africa','world/asia','world/europe','world/latin_america','world/middle_east',
'world/us_and_canada','england','northern_ireland','scotland','wales')

# Directories for the CNN news webpages I'm interested in
CNNArticleURLs = ('edition','edition_world','edition_africa','edition_americas',
'edition_asia','edition_europe','edition_meast','edition_us','money_news_international',
'edition_technology','edition_space','edition_entertainment','edition_sport',
'edition_football','edition_golf','edition_motorsport','edition_tennis')

# Directories for the CNN news webpages I'm interested in
RTArticleURLs = ('news', 'uk', 'usa', 'sport', 'russia', 'business')

def getArticles(dir, website):
    try:
        if website == 'BBC':
            tree = ET.parse(source=urllib.request.urlopen('http://feeds.bbci.co.uk/news/'+dir+'/rss.xml'))
        elif website == 'CNN':
            tree = ET.parse(source=urllib.request.urlopen('http://rss.cnn.com/rss/'+dir+'.rss'))
        elif website == 'RT':
            tree = ET.parse(source=urllib.request.urlopen('https://www.rt.com/rss/'+dir))
        else:
            tree = ET.parse(source=urllib.request.urlopen('https://www.theguardian.com/sitemaps/news.xml'))
    except HTTPError as err:
        print(err)
        return None
    except ET.ParseError as err:
        return None
    else:
        # Gets the xml tree as an object which
        # is then used to extract the articles
        root = tree.getroot()
        if website != 'guardian':
            allArticles = list()
            # TODO: fix issue with filtering bad titles
            # e.g 'RT UK News' or 'CNN.com - RSS' etc
            for elem in root.iter('title'):
                allArticles.append(elem.text)
            return allArticles
        else:
            i = 0
            if dir == 'titles':
                allTitles = list()
                for elem in root.iter('{http://www.google.com/schemas/sitemap-news/0.9}title'):
                    allTitles.append(elem.text.strip())
                    i += 1
                print('{} article titles scraped'.format(i))
                return allTitles

            else:
                # Returns a list where each element is a list containing
                # the keywords for an article title
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
            

def writeCSV(articleList, dir, invalid, website):
    if invalid:
        with open('errorLog.csv', 'a', encoding="utf-8") as file:
            fields = ['date', 'website', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'website':'{}'.format(website), 'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})
    else:
        with open('{}infoXML.csv'.format(website), 'a', encoding="utf-8") as file:
            fields = ['date', 'dir', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields,lineterminator='\n')

            for article in articleList:
                writeObj.writerow({'date':'{}'.format(currDate),'dir':'{}'.format(dir),'articleTitle':'{}'.format(article)})


def writeGuardianCSV(allTitles, allKeywords, date, invalid):
    if invalid:
        with open('errorLog.csv', 'a', encoding='utf-8') as file:
            i = 0
            fields = ['date', 'website', 'keywordsArr', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields, delimiter=',',lineterminator='\n')

            for title, keywords in zip(allTitles, allKeywords):
                writeObj.writerow({'date':'{}'.format(currDate), 'website':'{}'.format(website), 'keywordsArr':'{}'.format(keywords),'articleTitle':'{}'.format(title)})
                i += 1
    else:
        with open('guardianInfoXML.csv', 'a', encoding='utf-8') as file:
            i = 0
            fields = ['date','keywordsArr', 'articleTitle']
            writeObj = csv.DictWriter(file, fieldnames=fields, delimiter=',',lineterminator='\n')

            for title, keywords in zip(allTitles, allKeywords):
                writeObj.writerow({'date':'{}'.format(currDate),'keywordsArr':'{}'.format(keywords),'articleTitle':'{}'.format(title)})
                i += 1


def scrape(dir, website):
    if website != 'guardian':
        allArticles = getArticles(dir, website)
        if allArticles != None:
            writeCSV(allArticles, dir, 0, website)
            if website == 'BBC' or 'guardian' or 'RT':
                print('Downloaded articles from section: {} - {}'.format(website, dir))
            elif website == 'CNN':
                print('Downloaded articles from section: {} - {}'.format(website, dir[8:]))
        else:
            badscrapeMsg = 'Error could not scrape from section: {}'.format(dir)
            badscrape = list()
            badscrape.append(badscrapeMsg)
            writeCSV(badscrape, dir, 1, website)
            print('############ Failed to download articles from section: {} ############ '.format(dir))
    # If scraping from the guardian, slightly different format
    # due to the keywords list used
    if dir == 'titles':
        titlesList = getArticles('titles', 'guardian')
        return titlesList
    if dir == 'keywords': 
        keywordsList = getArticles('keywords', 'guardian')
        return keywordsList


def BBCControl():
    for target in BBCArticleURLs:
        scrape(target, 'BBC')
        time.sleep(random.random())


def CNNControl():
    for target in CNNarticleURLs:
        scrape(target, 'CNN')
        time.sleep(random.random())


def RTControl():
    for target in RTArticleURLs:
        scrape(target, 'RT')
        time.sleep(random.random())


def guardianControl():
    titlesList = scrape('titles', 'guardian')
    keywordsList = scrape('keywords', 'guardian')

    if titlesList and keywordsList != None:
        writeGuardianCSV(titlesList, keywordsList, currDate, 0)
    else:
        writeGuardianCSV(titlesList, keywordsList, currDate, 1)


def main():
    threading.Thread(target=BBCControl).start()
    threading.Thread(target=CNNControl).start()
    threading.Thread(target=guardianControl).start()
    threading.Thread(target=RTControl).start()
 
   
if __name__ == '__main__':
    main()