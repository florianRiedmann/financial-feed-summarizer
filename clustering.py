import pickle
import numpy as np
import matplotlib.pyplot as plt
import spacy
from sklearn import metrics
from sklearn.cluster import KMeans

from logger import logger
from config import GENERATE_NEW_VECTORS, VECTOR_PICKLE_FILE_NAME, SILHOUETTE_SCORE_PLOT_FILE_NAME, GLOBAL_RANDOM_SEED

np.random.seed(GLOBAL_RANDOM_SEED)

def load_core():
    logger.info("Loading spaCy Core")
    nlp = spacy.load('en_core_web_lg')  # loading spaCy core
    logger.info("spaCy Core loaded")
    return nlp


def vectorize_articles(article_list):
    nlp = load_core()
    docs = []
    logger.info("Vectorizing articles")
    for article in article_list:
        docs.append(nlp(' '.join(article)))
    logger.info(f"{len(article_list)} articles vectorized")
    return [doc.vector for doc in docs]


def save_vectors(data):
    logger.info(f"Pickling vectors to {VECTOR_PICKLE_FILE_NAME}")
    with open(VECTOR_PICKLE_FILE_NAME, "wb") as fp:
        pickle.dump(data, fp)
    logger.info("Vectors pickled")


def load_vectors():
    logger.info(f"Unpickling vectors from {VECTOR_PICKLE_FILE_NAME}")
    with open(VECTOR_PICKLE_FILE_NAME, "rb") as fp:
        data = pickle.load(fp)
    logger.info("Vectors unpickled")
    return data


def cluster_vectors(data):
    min_k = 10
    max_k = len(data)
    k_range = range(min_k, max_k)

    silhouette_scores = []
    models = []
    logger.info("Searching for optimal number of clusters")
    for k in k_range:
        model = KMeans(n_clusters=k)
        # model = Birch(branching_factor=50, n_clusters=k, threshold=0.1, compute_labels=True)
        model.fit(data)
        silhouette_scores.append(metrics.silhouette_score(data, model.labels_, metric='euclidean'))
        models.append(model)
    index_of_optimal_k = silhouette_scores.index(max(silhouette_scores))
    optimal_k = k_range[index_of_optimal_k]

    logger.info(f"Optimal number of Clusters is {optimal_k}")
    logger.info(f"Silhouette_score: {max(silhouette_scores)}")

    # Piloting silhouette_scores for demonstration purpose only
    plt.plot(k_range[:len(silhouette_scores)], silhouette_scores)
    plt.savefig(SILHOUETTE_SCORE_PLOT_FILE_NAME)

    return models[index_of_optimal_k].labels_  # returning list of cluster labels


def get_clusters(data):
    if GENERATE_NEW_VECTORS:
        vectors = vectorize_articles(data)
        save_vectors(vectors)
    else:
        vectors = load_vectors()
    return cluster_vectors(vectors)
