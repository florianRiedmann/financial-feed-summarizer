from logger import logger
from rank import summary
import pandas as pd


def get_summarized_articles(articles):
    articles = articles.groupby('cluster').agg({'article': 'sum', 'clean_article': 'sum'})
    summaries = []
    for i, article in articles.iterrows():
        clean_sentences = article['article']
        clean_clean_sentences = article['clean_article']
        logger.info(f"CLUSTER {i} SUMMARY")
        summarized_article = summary(clean_sentences, clean_clean_sentences)
        [print(f"{i + 1}: {elem}") for i, elem in enumerate(summarized_article)]
        summaries.append(summarized_article)
    articles['summary'] = pd.Series(summaries)
    return articles
