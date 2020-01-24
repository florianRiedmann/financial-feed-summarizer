import pandas as pd
from cleaner import get_clean_articles
from clustering import get_clusters
from config import SCRAPE_DATA, SCRAPED_DATA_FILE_NAME, CLEAN_ARTICLE_FILE_NAME, \
    CLUSTERED_ARTICLE_FILE_NAME, CLUSTER_ARTICLES, CHECK_DEPENDENCIES, CHECK_DIRECTORIES, \
    RESULTS_PATH, PICKLES_PATH, PLOTS_PATH, SUMMARIZE_ARTICLES, SUMMARIZED_ARTICLE_FILE_NAME, \
    GLOVE_PATH
from logger import logger
from readability_scorer import get_readability_score
from scraper import get_scraped_data
from directory import make_directory
from dependency import check_dependencies
from rank import summary


# STEP 1: Check Directories
from summerizer import get_summarized_articles

if CHECK_DIRECTORIES:
    logger.info("STEP 1: Checking for existing directories")
    make_directory(RESULTS_PATH, PICKLES_PATH, PLOTS_PATH, GLOVE_PATH)


# STEP 2: Check Dependencies
if CHECK_DEPENDENCIES:
    logger.info("STEP 2: Checking dependencies")
    check_dependencies()

# STEP 3: Scrapping data from RSS-Feeds
logger.info("STEP 3: Scrapping data from RSS-Feeds")
if SCRAPE_DATA:
    scraped_data = get_scraped_data()
    scraped_data.to_csv(SCRAPED_DATA_FILE_NAME, header=True)
else:
    scraped_data = pd.read_csv(SCRAPED_DATA_FILE_NAME, header=0)

# STEP 4: Cleaning articles
logger.info("STEP 4: Cleaning articles")
articles = get_clean_articles(scraped_data)
articles.to_csv(CLEAN_ARTICLE_FILE_NAME, header=True)

# STEP 5: Clustering articles
logger.info("STEP 5: Clustering articles")
if CLUSTER_ARTICLES:
    articles['cluster'] = get_clusters(articles['article'].to_list())
    articles.to_csv(CLUSTERED_ARTICLE_FILE_NAME, header=True)
else:
    articles = pd.read_csv(CLUSTERED_ARTICLE_FILE_NAME, header=0)

# STEP 6: Summarize articles
logger.info("STEP 6: Summarize articles")
if SUMMARIZE_ARTICLES:
    articles = get_summarized_articles(articles)
    articles.to_csv(SUMMARIZED_ARTICLE_FILE_NAME, header=True)
else:
    articles = pd.read_csv(SUMMARIZED_ARTICLE_FILE_NAME, header=0)


# STEP 7: Readability
logger.info("STEP 7: Get readability")
for i, article in articles.iterrows():
    summarized_text = article['summary']
    readability_score = get_readability_score(summarized_text)
    logger.info(f"CLUSTER {i}: Readability score: {readability_score}")

logger.info("THE END")
