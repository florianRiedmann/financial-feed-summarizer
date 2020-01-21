import sys
import os
from config import GLOVE_PATH, GLOVE_FILE_NAME


def check_dependencies():
    # Trying to load the required modules
    try:
        import matplotlib
        import numpy
        import pandas
        import sklearn
        import readability
        import feedparser
        import bs4
        import requests
        import logging
        import spacy
        import json
        import networkx
        import nltk
        nltk.download('punkt')
        nltk.download('stopwords')
    except ModuleNotFoundError:
        sys.exit('Missing Dependency: Install packages with "pip install -r requirements.txt"')

    # Trying to load the spaCy core model
    try:
        assert spacy.load('en_core_web_lg')
    except AssertionError:
        sys.exit('Missing Dependency: Install spacy model with "python -m spacy download en_core_web_lg"')

    # Checking for Glove
    try:
        assert os.path.exists(os.path.join(GLOVE_PATH, GLOVE_FILE_NAME))
    except AssertionError:
        sys.exit(f'Missing Dependency: Download Glove from "http://nlp.stanford.edu/data/glove.6B.zip" and unzip to {GLOVE_PATH}')
