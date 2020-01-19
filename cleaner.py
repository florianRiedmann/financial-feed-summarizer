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


# remove empty articles from the dataFrame
def remove_empty_articles(data):
    empty_article = []
    for index, article in data['article'].items():
        if not article: # check if it is a empty string
            empty_article.append(index) # append the index of the row
    data = data.drop(empty_article)
    return data

def tokenize_articles(data):
    # makes a list with a list of tokenized articles
    articles = []
    for article in data['article']:
        articles.append(sent_tokenize(str(article)))
    return pd.Series(articles)

def make_list_sentences(data):
    # make a list with every sentence
    sentences = []
    for article in data:
        for sentence in article:
            sentences.append(sentence)
    return pd.Series(sentences)

def remove_bad_words(data):
    # Remove sentences with bad_words
    bad_words = ['seeking', 'premium', 'subscribe', 'payable', 'follow', 'submitted', 'copyright']
    for index, sentence in data.items():
        for word in sentence.replace(".", " ").replace(";", " ").replace("\'", " ").split(" "):
            if word.lower() in bad_words:
                data = data.drop(index)
                break # continue with the outer loop
    return data

def remove_short_sentences(data):
    # sentence length has to be minimum of three words after cleaning
    data = pd.Series([sentence for sentence in data if len(sentence.split(" ")) >= 5])
    return data

def remove_duplicate_sentences(data):
    # remove duplicates from scentences
    data = data.drop_duplicates(keep='first')
    return data

def clean_sentence(data):
    data = pd.Series(data).str.replace(r"[\[\]]", "", regex=True) \
        .str.replace(",\'", "", regex=False) \
        .str.replace("\',", "", regex=False) \
        .str.replace("\",", "", regex=False) \
        .str.replace("\"", "", regex=False) \
        .str.replace(r"^ ", "", regex=True) \
        .str.replace(r"^\'", "", regex=True)
    return data

def clean_clean_sentence(data):
    # remove numbers, spaces, special characters and punctuation
    series = pd.Series(data).str.replace("[^a-zA-Z]", " ") \
        .str.replace("\s+", " ") \
        .str.replace("^\s", "") \
        .str.replace("\s$", "")
    data = pd.concat([data, series], axis=1)
    return data

def lowercase_sentences(data):
    # change to lowercase
    data.iloc[:,1] = data.iloc[:,1].str.lower()
    return data

def remove_stopwords(data):
    # remove stopwords
    sentences = data.iloc[:,1].tolist()
    stop_words = stopwords.words('english')
    filtered_sentences = []
    for sentence in sentences:
        filtered_words = []
        for word in sentence.split(" "):
            if word not in stop_words:
                filtered_words.append(word)
        filtered_sentences.append(" ".join(filtered_words))
        data.iloc[:,1] = pd.Series(filtered_sentences)
    return data

# cleaning pipline
def clean_sentence_pipe():
    return (scraper.create_DataFrame()
            .pipe(remove_empty_articles)
            .pipe(tokenize_articles)
            .pipe(make_list_sentences)
            .pipe(remove_bad_words)
            .pipe(remove_short_sentences)
            .pipe(remove_duplicate_sentences)
            .pipe(clean_sentence))

def clean_clean_sentence_pipe():
    return (clean_sentence_pipe()
            .pipe(clean_clean_sentence)
            .pipe(lowercase_sentences)
            .pipe(remove_stopwords))
