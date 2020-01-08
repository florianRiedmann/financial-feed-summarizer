import glob
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import logging
import time
import matplotlib.pyplot as plt
import os
import re

early_stopping = False
early_stopping_step = 6
max_k = 6
np.random.seed(1)

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

project_dir = os.path.dirname(__file__)
files = glob.glob(os.path.join(project_dir, "*/*.csv"))
feeds = []
for file in files:
    feeds.append(pd.read_csv(file))
feed_df = pd.concat(feeds, axis=0, ignore_index=True, sort=True)
feed_df['article'].to_csv(os.path.join(project_dir, "clusteredText/Texts_not_cleaned.csv"))

texts = feed_df['article'].dropna().replace(r'\\n', ' ', regex=True) \
    .replace(r'\[', '', regex=True) \
    .replace(r'\]', '', regex=True) \
    .replace(r'\\r', '', regex=True) \
    .replace(r'\\n', '', regex=True) \
    .replace(r'\\t', '', regex=True) \
    .replace(r"\'", '', regex=True) \
    .replace(r"\"", "", regex=True) \

texts = texts.replace('[^a-zA-Z]', '')
pd.DataFrame(texts).to_csv(os.path.join(project_dir, "clusteredText/Texts_cleaned.csv"))

texts = texts.tolist()

# texts = [
#     "Penny bought bright blue fishes.",
#     "Penny bought bright blue and orange fish.",
#     "The cat ate a fish at the store.",
#     "Penny went to the store. Penny ate a bug. Penny saw a fish.",
#     "It meowed once at the bug, it is still meowing at the bug and the fish",
#     "The cat is at the fish store. The cat is orange. The cat is meowing at the fish.",
#     "Penny is a fish",
#     "A house is not a mouse",
#     "Mikey mouse was a huge star",
#     "House of cards is a tv show",
#     "Michael Knight is fighting for right.",
#     "The Knight Foundation is providing for peace",
# ]

vec = TfidfVectorizer(stop_words='english', use_idf=True)
matrix = vec.fit_transform(texts)
idf_df = pd.DataFrame(matrix.toarray(), columns=vec.get_feature_names())

silhouettes = []
distortions = []
K = range(2, max_k)

start_time = int(time.time() * 1000)

# for k in K:
#     print(f"k is {k}")
#     model = KMeans(n_clusters=k)
#     model.fit(matrix)
#     silhouettes.append(silhouette_score(matrix, model.labels_, metric='euclidean'))
#     if early_stopping:
#         if k > early_stopping_step+1 and silhouettes[-1] < silhouettes[-1-early_stopping_step]:
#             break
#
# print(f"time elapsed {int(time.time() * 1000) - start_time}ms")
#
# if early_stopping:
#     optimal_k = silhouettes.index(max(silhouettes)) + early_stopping_step
# else:
#     optimal_k = silhouettes.index(max(silhouettes))
#
# print(f"Optimal K is {optimal_k,}")
#
# model = KMeans(n_clusters=optimal_k)
# model.fit(matrix)
#
# results = pd.DataFrame()
# results['text'] = texts
# results['category'] = model.labels_
#
# print(results)
# print(results.groupby('category').count())
#
# plt.plot(K[:len(silhouettes)], silhouettes)
# plt.show()
#
# results.to_csv(os.path.join(project_dir, "clusteredText/Text1.csv"))
