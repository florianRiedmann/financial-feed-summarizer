import nltk
import pandas as pd
from logger import logger
import scraper
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


# remove empty articles from the dataFrame
def remove_empty_articles(data):
    logger.info("removing empty articles")
    empty_article = []
    for index, article in data['article'].items():
        if not article:  # check if it is a empty string
            empty_article.append(index)  # append the index of the row
    data = data.drop(empty_article)
    return data


def tokenize_articles(data):
    logger.info("tokenizing articles")
    # makes a list with a list of tokenized articles
    articles = []
    for article in data['article']:
        articles.append(sent_tokenize(str(article)))
    data['tokenized_articles'] = articles
    return data


def make_list_sentences(data):
    logger.info("generating sentence list")
    # make a list with every sentence
    sentences = []
    article_nrs = []
    for index, article in data['tokenized_articles'].items():
        for sentence in article:
            sentences.append(sentence)
            article_nrs.append(index)
    return pd.DataFrame(list(zip(sentences, article_nrs)), columns=['sentences', 'article_nr'])


def remove_bad_words(data):
    logger.info("removing bad sentences")
    # Remove sentences with bad_words
    bad_words = ['seeking', 'premium', 'subscribe', 'payable', 'follow', 'submitted', 'copyright']
    for index, sentence in data['sentences'].items():
        for word in sentence.replace(".", " ").replace(";", " ").replace("\'", " ").split(" "):
            if word.lower() in bad_words:
                data = data.drop(index)
                break  # continue with the outer loop
    return data


def remove_short_sentences(data):
    logger.info("removing short sentences")
    # sentence length has to be minimum of three words after cleaning
    data['sentences'] = pd.Series([sentence for sentence in data['sentences'] if len(sentence.split(" ")) >= 5])
    data = data.dropna()
    return data


def remove_duplicate_sentences(data):
    logger.info("removing duplicated sentences")
    # remove duplicates from scentences
    print(len(data))
    sentences = list(set(data))
    print(len(data))
    return data


def clean_sentence(data):
    logger.info("cleaning sentences")
    data['sentences'] = pd.Series(data['sentences']).str.replace(r"[\[\]]", "", regex=True) \
        .str.replace(",\'", "", regex=False) \
        .str.replace("\',", "", regex=False) \
        .str.replace("\",", "", regex=False) \
        .str.replace("\"", "", regex=False) \
        .str.replace(r"^ ", "", regex=True) \
        .str.replace(r"^\'", "", regex=True)
    return data


def clean_clean_sentence(data):
    # remove numbers, spaces, special characters and punctuation
    data['clean_sentences'] = pd.Series(data['sentences']).str.replace("[^a-zA-Z]", " ") \
        .str.replace("\s+", " ") \
        .str.replace("^\s", "") \
        .str.replace("\s$", "")
    return data


def lowercase_sentences(data):
    # change to lowercase
    data['clean_sentences'] = data['clean_sentences'].str.lower()
    return data


def remove_stopwords(data):
    # remove stopwords
    stop_words = stopwords.words('english')
    filtered_sentences = []
    for sentence in data['clean_sentences']:
        filtered_words = []
        for word in sentence.split(" "):
            if word not in stop_words:
                filtered_words.append(word)
        filtered_sentences.append(" ".join(filtered_words))
    data['clean_sentences'] = filtered_sentences
    return data
  

def combine_to_article(data):
    grp = data.groupby('article_nr')
    articles = pd.DataFrame()
    articles['article'] = grp['sentences'].apply(list)
    articles['clean_article'] = grp['clean_sentences'].apply(list)
    return articles


# cleaning pipline
def clean_sentence_pipe():
    return (scraper.get_scraped_data()
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


def clean_article_pipe(data):
    return (data
            .pipe(remove_empty_articles)
            .pipe(tokenize_articles)
            .pipe(make_list_sentences)
            .pipe(remove_bad_words)
            .pipe(remove_short_sentences)
            .pipe(clean_sentence)
            .pipe(clean_clean_sentence)
            .pipe(lowercase_sentences)
            .pipe(remove_stopwords)
            .pipe(combine_to_article))

