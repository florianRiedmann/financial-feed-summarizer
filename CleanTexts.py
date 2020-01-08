import glob
import os
import re

import nltk
import pandas as pd

nltk.download('stopwords')

from nltk.corpus import stopwords


project_dir = os.path.dirname(__file__)
files = glob.glob(os.path.join(project_dir, "*/*.csv"))
feeds = []
for file in files:
    feeds.append(pd.read_csv(file))
feed_df = pd.concat(feeds, axis=0, ignore_index=True, sort=True)
feed_df['article'] = feed_df['article'].dropna()
feed_df['article'].to_csv(os.path.join(project_dir, "clusteredText/Texts_not_cleaned.csv"))

feed_df['article'] = feed_df['article'].dropna().replace(r'\\n', ' ', regex=True) \
    .replace(r'\\r', '', regex=True) \
    .replace(r'\\n', '', regex=True) \
    .replace(r'\\t', '', regex=True)

corpus = [] # List for storing cleaned data
ps = nltk.PorterStemmer() #Initializing object for stemming
for i in range(len(feed_df)): # for each obervation in the dataset
   #Removing special characters
   text = re.sub('[^a-zA-Z]', ' ', feed_df['article'][i]).lower().split()
   #Stemming and removing stop words
   text = [word for word in text if not word in set(stopwords.words('english'))]
   #Joining all the cleaned words to form a sentence
   text = ' '.join(text)
   #Adding the cleaned sentence to a list
   corpus.append(text)

print(corpus)
pd.DataFrame(corpus).to_csv(os.path.join(project_dir, "clusteredText/Texts_cleaned.csv"))



