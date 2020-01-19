import os
import numpy as np
import pandas as pd
import networkx as nx
import cleaner
import export

# import clean sentences and clean clean sentences and find rows with nan -> drop them
df = cleaner.clean_clean_sentence_pipe().dropna()

# word_vectors
# import pre-trained word_vectors from glove
def get_word_vectors():
    path = "glove/glove.6B.100d.txt"
    word_vectors = {}
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
            sum = np.zeros((100,))
            words = i.split()
            for j in words:
                if j in word_vectors.keys():
                    vector = word_vectors[j]
                    sum = sum + vector
                else:
                    sum = sum + np.zeros((100,))
            avg = sum / len(words)
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
    for i in range(n):
      for j in range(n):
        if i != j:
          S[i][j] = cosine_similarity(sentence_vectors[i], sentence_vectors[j])
    return S

def summary(data):
    list = []
    print(data.head())
    clean_sentence = data.iloc[:,0]
    clean_clean_sentence = data.iloc[:,1]

    # Pagerank Algorithm
    # https://networkx.github.io/documentation/networkx-1.9.1/overview.html
    G = nx.from_numpy_array(make_similarity_matrix(clean_clean_sentence))
    scores = nx.pagerank(G)

    for index, sentence in enumerate(clean_sentence): # Tuples of the score and the sentence
        list.append((scores[index], sentence))

    data = pd.DataFrame(list, columns =['Score', 'Sentence'])
    return data

export.export_summary(summary(df))
