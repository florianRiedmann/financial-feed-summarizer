import os
import feedparser
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import datetime
import json

with open('feeds.json') as file:
    feeds = json.load(file)

def parse_feed(feed: dict):
    title, url, date = ([] for i in range(3))
    f = feedparser.parse(feed['url'])
    for entry in f.entries:
        title.append(entry.title)
        url.append(entry.link)
        date.append(entry.published)
    return  {'title': title, 'url': url, 'date': date}


def clean_string(s: str):
    s = re.sub(pattern=r'\([^)]*\)|\xa0', repl='', string=s)
    return s


def get_article(parsedFeed: dict, tag=None, classOfTag=None, headers=None):
    listOfArticles = []
    urls = parsedFeed['url']
    for url in urls:
        try:
            article = []
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find(name=tag, class_=classOfTag).find_all('p')
            for paragraph in paragraphs:
                paragraph = paragraph.get_text()
                paragraph = clean_string(paragraph)
                article.append(paragraph)
        except AttributeError:
            print('Attribute Error!')
        listOfArticles.append(article)
    parsedFeed['article'] = listOfArticles
    return parsedFeed


def make_directory(path: str):
    currentDirectory = os.getcwd()
    try:
        os.makedirs(f"{currentDirectory}/{path}")
    except FileExistsError:
        # directory already exists
        pass
    return f'{currentDirectory}/{path}'


def create_DataFrame(feeds):
    dataFrame = pd.DataFrame()
    date = datetime.date.today()
    for id, feed in feeds.items():
        d = parse_feed(feed)
        d = get_article(d, tag=feed['tag'], classOfTag=feed['class'], headers=feed['header'])
        df = pd.DataFrame(d)
        df.to_csv(f'{make_directory(str(date))}/{date}_financial_feed_id_{id}.csv', index=False)
        dataFrame = pd.concat([dataFrame, df])
    return dataFrame


create_DataFrame(feeds)
