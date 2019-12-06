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

d = feedparser.parse('https://seekingalpha.com/market_currents.xml')
print(d)
