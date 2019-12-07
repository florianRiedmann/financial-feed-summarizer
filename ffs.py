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
                    #'https://www.investing.com/rss/news.rss',
                    #'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
                    #'https://www.cnbc.com/id/10000664/device/rss/rss.html'
                    ]

newsLinks = {'title': [], 'link': []}

# Getting titles and links from the RSS-Feeds and saving into the newsLinks dict
for feedLink in financialFeeds:
    d = feedparser.parse(feedLink)
    for entry in d.entries:
        newsLinks['title'].append(entry.title)
        newsLinks['link'].append(entry.link)

# Getting the article text from the link and saving it to the DataFrame (only functional with seekingalpha atm)
article = []

for link in newsLinks['link']:
    paragraphText = []
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.article:
        paragraphs = soup.article.find_all('p')
        for paragraph in paragraphs:
            paragraphText.append(paragraph.get_text())
        article.append(paragraphText)
    else:
        article.append(np.nan)

# Adding paragraph text to the newsLinks dict
newsLinks['text'] = article

# Converting the dict to a DataFrame and change column order
financialFeedsDataFrame = pd.DataFrame.from_dict(newsLinks)
order = ['title', 'link', 'text']
financialFeedsDataFrame = financialFeedsDataFrame.loc[:,order]

# Export DataFrame to a csv file
financialFeedsDataFrame.to_csv('financialFeeds.csv', index=False)
