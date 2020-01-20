import json
import os
import re

import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup

project_dir = os.path.dirname(__file__)

def get_feeds(filename):
    with open(os.path.join(project_dir, filename)) as file:
        dict = json.load(file)
    return dict


def parse_feeds(dict):
    title, url, date = ([] for i in range(3))
    f = feedparser.parse(dict['url'])
    for entry in f.entries:
        title.append(entry.title)
        url.append(entry.link)
        date.append(entry.published)
    dict = {'title': title, 'url': url, 'date': date}
    return dict


def get_article(dict, tag=None, class__=None, headers=None):
    articles = []
    urls = dict['url']
    for url in urls:
        try:
            article = []
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find(name=tag, class_=class__).find_all('p')
            for paragraph in paragraphs:
                paragraph = paragraph.get_text().strip()
                # cleaning for business-standard.com
                paragraph = re.sub(r";", " ", paragraph) # remove semicolons
                paragraph = re.sub(r"\s+", " ", paragraph) # remove whitespace
                paragraph = re.sub(r"(?<=.document)(.*)(?=Banner=1)", "", paragraph) # remove googletags
                paragraph = paragraph.replace(".documentBanner=1", "")
                article.append(paragraph)
        except AttributeError:
            print(url)
            print('Attribute Error!')
        articles.append(article)
    dict['article'] = articles
    return dict


def get_scraped_data():
    feeds = get_feeds('feeds.json')
    data = pd.DataFrame()
    for index, feed in feeds.items():
        d = parse_feeds(feed)
        d = get_article(d, tag=feed['tag'], class__=feed['class'], headers=feed['header'])
        df = pd.DataFrame(d)
        data = pd.concat([data, df])
    return data
