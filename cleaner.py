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
feed_df = scraper.create_DataFrame(scraper.feeds(), export_csv=False)
# feed_df = pd.read_csv(os.path.join(project_dir,'2020-01-09/2020-01-09_financial_feed_id_1.csv'))

# remove empty articles from the dataFrame
empty_article = []
for index, article in feed_df['article'].items():
    if not article: # check if it is a empty string
        empty_article.append(index) # append the index of the row

feed_df = feed_df.drop(empty_article)

articles = []
for article in feed_df['article']:
    articles.append(sent_tokenize(str(article)))

# make a list with every sentence
sentences = []
for article in articles:
    for sentence in article:
        sentences.append(sentence)

# Remove sentences with bad_words
bad_words = ['seeking', 'premium', 'subscribe', 'payable', 'follow', 'googletag']


for sentence in sentences:
    for word in sentence.replace(".", " ").replace(";", " ").split(" "):
        if word in bad_words:
            sentences.remove(sentence)
            break # continue with the outer loop

# sentence length has to be minimum of three words after cleaning
sentences = [sentence for sentence in sentences if len(sentence.split(" ")) >= 5]



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

# export cleaned sentences do DataFrame
pd.DataFrame(sentences).to_csv(os.path.join(project_dir, "clean_text/sentences.csv"), header=False, index=False)
pd.DataFrame(clean_sentences).to_csv(os.path.join(project_dir, "clean_text/clean_sentences.csv"), header=False, index=False)
