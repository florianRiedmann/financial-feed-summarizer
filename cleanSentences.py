import glob
import os
import re
import scraper
import pandas as pd

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

project_dir = os.path.dirname(__file__)
feed_df = pd.read_csv(os.path.join(project_dir,'2020-01-09/2020-01-09_financial_feed_id_0.csv'))
# feed_df = scraper.create_DataFrame(scraper.feeds())

# returns a list of articles with a list of sentences in it
articles = [sent_tokenize(article) for article in feed_df['article']]

sentences = []
for article in articles:
    for sentence in article:
        sentences.append(sentence)

# remove numbers, spaces, special characters and punctuation
clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ") \
    .str.replace("\s+", " ") \
    .str.replace("^\s", "") \
    .str.replace("\s$", "")

# change to lowercase
clean_sentences = [str.lower(s) for s in clean_sentences]

# remove stopwords
stop_words = stopwords.words('english')
filtered_sentences = []
for sentence in clean_sentences:
    filtered_words = []
    for word in sentence.split(" "):
        if word not in stop_words:
            filtered_words.append(word)
    filtered_sentences.append(" ".join(filtered_words))

# sentence length has to be minimum of three words after cleaning
clean_sentences = [sentence if len(sentence.split(" ")) >= 3 else "" for sentence in filtered_sentences ]

# export cleaned sentences do DataFrame
pd.DataFrame(sentences).to_csv(os.path.join(project_dir, "clean_text/sentences.csv"), header=False, index=False)
pd.DataFrame(clean_sentences).to_csv(os.path.join(project_dir, "clean_text/clean_sentences.csv"), header=False, index=False)
