import json
import os
import re
import feedparser
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import PROJECT_DIR, JSON_FILE_NAME
from logger import logger


def get_feeds(filename):
    with open(os.path.join(PROJECT_DIR, filename)) as file:
        data = json.load(file)
    return data


def parse_feeds(data):
    title, url, date = [], [], []
    f = feedparser.parse(data['url'])
    for entry in f.entries:
        title.append(entry.title)
        url.append(entry.link)
        date.append(entry.published)
    data = {'title': title, 'url': url, 'date': date}
    return data


def get_article(d, tag=None, class__=None, headers=None):
    articles = []
    urls = d['url']
    for url in urls:
        try:
            a = []
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find(name=tag, class_=class__).find_all('p')
            for paragraph in paragraphs:
                paragraph = paragraph.get_text().strip()
                # cleaning for business-standard.com
                paragraph = re.sub(r';', " ", paragraph)  # remove semicolons
                paragraph = re.sub(r'\s+', " ", paragraph)  # remove whitespace
                paragraph = re.sub(r'(?<=.document)(.*)(?=Banner=1)', "", paragraph)  # remove google-tags
                paragraph = paragraph.replace(".documentBanner=1", "")  # remove string
                a.append(paragraph)
        except AttributeError:
            logger.info(f"ATTENTION: {url} is corrupted")
        articles.append(a)
    d['article'] = articles
    return d


def get_scraped_data():
    feeds = get_feeds(JSON_FILE_NAME)
    data = pd.DataFrame()
    for index, feed in feeds.items():
        d = parse_feeds(feed)
        d = get_article(d, tag=feed['tag'], class__=feed['class'], headers=feed['header'])
        df = pd.DataFrame(d)
        data = pd.concat([data, df])
    return data
