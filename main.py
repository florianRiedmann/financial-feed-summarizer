import pandas as pd

from cleaner import clean_sentence_pipe, clean_article_pipe
from clustering import get_clusters
from config import SCRAPE_DATA, SCRAPED_DATA_FILE_NAME, CLEAN_ARTICLE_FILE_NAME, CLEAN_SENTENCE_FILE_NAME, \
    CLUSTERED_ARTICLE_FILE_NAME, CLUSTER_ARTICLES
from logger import logger
from scraper import get_scraped_data

# STEP 1: Scrapping data from RSS-Feeds
logger.info("STEP 1: Scrapping data from RSS-Feeds")
if SCRAPE_DATA:
    scraped_data = get_scraped_data()
    scraped_data.to_csv(SCRAPED_DATA_FILE_NAME, header=True)
else:
    scraped_data = pd.read_csv(SCRAPED_DATA_FILE_NAME, header=0)

# STEP 2: Cleaning articles
logger.info("STEP 2: Cleaning articles")
articles = clean_article_pipe(scraped_data)
articles.to_csv(CLEAN_ARTICLE_FILE_NAME, header=True)

# STEP 3: Clustering articles
logger.info("STEP 3: Clustering articles")
if CLUSTER_ARTICLES:
    articles['cluster'] = get_clusters(articles['article'].to_list())
    articles.to_csv(CLUSTERED_ARTICLE_FILE_NAME, header=True)
else:
    articles = pd.read_csv(CLUSTERED_ARTICLE_FILE_NAME, header=0)

# STEP 4: Summarize articles
logger.info("STEP 4: Summarize articles")
grp = articles.groupby('cluster')
articles = articles.groupby('cluster').agg({'article': 'sum', 'clean_article': 'sum'})

for i, article in articles.iterrows():
    # clean_sentences = article['article']
    # clean_clean_sentences = article['clean_article']
    # text rank cluster an summerize
    print()

logger.info("THE END")
