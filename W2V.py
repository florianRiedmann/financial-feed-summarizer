import glob
import os
import re

import pandas as pd
from gensim.models import Word2Vec

from nltk.cluster import KMeansClusterer
import nltk
import numpy as np

from sklearn import cluster
from sklearn import metrics

# training data

sentences = [['this', 'is', 'the', 'one', 'good', 'machine', 'learning', 'book'],
             ['this', 'is', 'another', 'book'],
             ['one', 'more', 'book'],
             ['weather', 'rain', 'snow'],
             ['yesterday', 'weather', 'snow'],
             ['forecast', 'tomorrow', 'rain', 'snow'],
             ['this', 'is', 'the', 'new', 'post'],
             ['this', 'is', 'about', 'more', 'machine', 'learning', 'post'],
             ['and', 'this', 'is', 'the', 'one', 'last', 'post', 'book']]

sentences = []

project_dir = os.path.dirname(__file__)
files = glob.glob(os.path.join(project_dir, "*/*.csv"))
feeds = []
for file in files:
    feeds.append(pd.read_csv(file))
feed_df = pd.concat(feeds, axis=0, ignore_index=True)
texts = feed_df['article'].dropna().replace(r'\\n', ' ', regex=True) \
    .replace(r'\[', '', regex=True) \
    .replace(r'\]', '', regex=True) \
    .replace(r'\\r', '', regex=True) \
    .replace(r'\\t', '', regex=True) \
    .replace(r"\'", '', regex=True)    \
    .replace(r"\"", "", regex=True) \
    .tolist()
for text in texts:
    if text:
        sentences.append(re.sub(r"[^a-zA-Z0-9]+", ' ', text))

model = Word2Vec(sentences, min_count=1)


def sent_vectorizer(sent, model):
    sent_vec = []
    numw = 0
    for w in sent:
        try:
            if numw == 0:
                sent_vec = model[w]
            else:
                sent_vec = np.add(sent_vec, model[w])
            numw += 1
        except:
            pass

    return np.asarray(sent_vec) / numw


X = []
for sentence in sentences:
    X.append(sent_vectorizer(sentence, model))

print("========================")
print(X)

# note with some version you would need use this (without wv)
#  model[model.vocab]
print(model[model.wv.vocab])

# print(model.similarity('post', 'book'))
# print(model.most_similar(positive=['machine'], negative=[], topn=2))

NUM_CLUSTERS = 5
kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
print(assigned_clusters)

for index, sentence in enumerate(sentences):
    print(str(assigned_clusters[index]) + ":" + str(sentence))

kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS)
kmeans.fit(X)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("Cluster id labels for inputted data")
print(labels)
print("Centroids data")
print(centroids)

print(
    "Score (Opposite of the value of X on the K-means objective which is Sum of distances of samples to their closest cluster center):")
print(kmeans.score(X))

silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')

print("Silhouette_score: ")
print(silhouette_score)

import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)

Y = model.fit_transform(X)

plt.scatter(Y[:, 0], Y[:, 1], c=assigned_clusters, s=290, alpha=.5)


for j in range(len(sentences)):
    plt.annotate(assigned_clusters[j], xy=(Y[j][0], Y[j][1]), xytext=(0, 0), textcoords='offset points')
    print("%s %s" % (assigned_clusters[j], sentences[j]))

plt.show()