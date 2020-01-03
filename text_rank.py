import numpy as np
import pandas as pd
import nltk

df = pd.read_csv('2019-12-13/2019-12-13_financial_feed_id_0.csv')

#nltk.download()

from nltk.tokenize import sent_tokenize

sentences = []
for s in df.article:
    sentences.append(sent_tokenize(s))

sentences = [y for x in sentences for y in x]

clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]"," ")
clean_sentences = [s.lower() for s in clean_sentences]
clean_sentences = pd.Series(clean_sentences).str.replace(' +', ' ')

#clean_sentences.str.replace(' +', ' ')

print(len(clean_sentences))
print(clean_sentences.head())

# remove stopwords
# word vectors
# model
