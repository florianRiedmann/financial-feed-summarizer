import numpy as np
import pandas as pd
import networkx as nx
from logger import logger
from config import SUMMARY_SENTENCE_NUMBER, GLOBAL_RANDOM_SEED

np.random.seed(GLOBAL_RANDOM_SEED)

# word_vectors
# import pre-trained word_vectors from glove
def get_word_vectors():
    word_vectors = {}
    path = "glove/glove.6B.100d.txt"
    with open(file=path, mode='r') as file:
        for line in file:
            values = line.split()
            word = values[0]
            coefficients = np.array(values[1:], dtype='float32')
            word_vectors[word] = coefficients
    return word_vectors


# Averaging the word_vectors for the sentence_vector
# https://cs.stanford.edu/~quocle/paragraph_vector.pdf
# https://www.aclweb.org/anthology/P16-1089.pdf
# https://nlp.stanford.edu/~socherr/EMNLP2013_RNTN.pdf
def make_sentence_vectors(data):
    word_vectors = get_word_vectors()
    sentence_vectors = []
    for i in data:
        if len(i) != 0:
            s = np.zeros((100,))
            words = i.split()
            for j in words:
                if j in word_vectors.keys():
                    vector = word_vectors[j]
                    s = s + vector
                else:
                    s = s + np.zeros((100,))
            avg = s / len(words)
        else:
            avg = np.zeros((100,))
        sentence_vectors.append(avg)
    return sentence_vectors


def cosine_similarity(v1, v2):
    dot = np.dot(v1, v2)
    normv1 = np.linalg.norm(v1)
    normv2 = np.linalg.norm(v2)
    cos = dot / (normv1 * normv2)
    return cos


def make_similarity_matrix(data):
    # call the make sentence vector function
    sentence_vectors = make_sentence_vectors(data)

    # empty matrix
    n = len(data)
    S = np.zeros([n, n])

    # http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
    # Cosine similarity between sentence_vectors (cosine similarity: 1 - cosine distance)
    # https://cmry.github.io/notes/euclidean-v-cosine
    for i in range(n):
        for j in range(n):
            if i != j:
                S[i][j] = cosine_similarity(sentence_vectors[i], sentence_vectors[j])
    return S


def summary(s1, s2):
    logger.info("INFO: Calculating summary...")
    s = []
    # pagerank Algorithm
    # https://networkx.github.io/documentation/networkx-1.9.1/overview.html
    G = nx.from_numpy_array(make_similarity_matrix(s2))
    scores = nx.pagerank(G)

    # align the scores with the sentences
    for index, sentence in enumerate(s1):  # Tuples of the score and the sentence
        s.append((scores[index], sentence))

    # Summary is the top 5 sentences of the article
    data = pd.DataFrame(s, columns=['Score', 'Sentence']).nlargest(SUMMARY_SENTENCE_NUMBER, 'Score')
    data = data['Sentence'].to_list()
    return data
