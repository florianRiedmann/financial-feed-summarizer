# RSS FEEDS

# https://seekingalpha.com/market_currents.xml              seekingalpha.com
# https://www.investing.com/rss/news.rss                    Investing.com
# https://feeds.a.dj.com/rss/RSSMarketsMain.xml             Wall Stree Journal
# https://www.cnbc.com/id/10000664/device/rss/rss.html      CNBC Finance

# Crawl serveral financial feeds
# Python Package feedparser

# Determine similarity
# Jaccard coefficient, Lexical similarity
# Semantic similarity?

# Create readable 'new' text (Summaries)
# extractive summarization
# abstractive summarization

# Text Rank Algorithm

import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

financialFeeds = [  'https://seekingalpha.com/market_currents.xml',
                    'https://www.investing.com/rss/news.rss',
                    'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
                    'https://www.cnbc.com/id/10000664/device/rss/rss.html'
                    ]



# Getting titles and links from the RSS-Feeds and saving into arrays
title = []
link = []
for feedLink in financialFeeds:
    d = feedparser.parse(feedLink)
    for entry in d.entries:
        title.append(entry.title)
        link.append(entry.link)

# Getting the article text with bs4 from the link list and saving it into an array called text
# Functions for four different news sites
def get_article_from_seeking(url):
    article = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.article.find_all('p')
    for paragraph in paragraphs:
        article.append(paragraph.get_text())
    return article

def get_article_from_investing(url):
    article = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find("div", class_="WYSIWYG articlePage").find_all('p')
    for paragraph in paragraphs:
        article.append(paragraph.get_text())
    return article

def get_article_from_wsj(url):
    article = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find("div", class_="group").find_all('p')
    for paragraph in paragraphs:
        article.append(paragraph.get_text())
    return article

def get_article_from_cnbc(url):
    article = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find("div", class_="group").find_all('p')
    for paragraph in paragraphs:
        article.append(paragraph.get_text())
    return article

text = []
for url in link:
    try:
        if url.find('seekingalpha.com') != -1:
            text.append(get_article_from_seeking(url))
        elif url.find('investing.com') != -1:
            text.append(get_article_from_investing(url))
        elif url.find('www.wsj.com') != -1:
            text.append(get_article_from_wsj(url))
        elif url.find('www.cnbc.com') != -1:
            text.append(get_article_from_cnbc(url))
        else:
            print('Else')
            text.append(np.nan)
    except AttributeError:
        print('Error')
        text.append(np.nan)

print(len(text))

# Adding arrays to a dict
newsLinks = {'title': title, 'link': link, 'text': text}

# Converting the dict to a DataFrame and change column order
financialFeedsDataFrame = pd.DataFrame.from_dict(newsLinks)
order = ['title', 'link', 'text']
financialFeedsDataFrame = financialFeedsDataFrame.loc[:,order]

# Export DataFrame to a csv file
financialFeedsDataFrame.to_csv('financialFeeds.csv', index=False)
