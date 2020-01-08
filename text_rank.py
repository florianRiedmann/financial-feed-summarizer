import os
import numpy as np
import pandas as pd
import networkx as nx

sentences = pd.read_csv('test_data/sentences.csv', header=None, squeeze=True)
clean_sentences = pd.read_csv('test_data/clean_sentences.csv', header=None, squeeze=True)

# find rows with nan
mask = clean_sentences.isna()
nan_rows = clean_sentences[mask].index.tolist()

sentences.drop(nan_rows, inplace=True)
clean_sentences.drop(nan_rows, inplace=True)
sentences = sentences.tolist()
clean_sentences = clean_sentences.tolist()


# word_vectors
# import pre-trained word_vectors from glove
def get_word_vectors(filepath):
    word_vectors = {}
    with open(file=filepath, mode='r') as file:
        for line in file:
            values = line.split()
            word = values[0]
            coefficients = np.array(values[1:], dtype='float32')
            word_vectors[word] = coefficients
    return word_vectors

word_vectors = get_word_vectors(filepath='glove/glove.6B.100d.txt')

# Averaging the word_vectors for the sentence_vector
# https://cs.stanford.edu/~quocle/paragraph_vector.pdf
# https://www.aclweb.org/anthology/P16-1089.pdf
# https://nlp.stanford.edu/~socherr/EMNLP2013_RNTN.pdf

sentence_vectors = []
for i in clean_sentences:
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

# Similarity Matrix
n = len(sentences)
S = np.zeros([n, n])

def cosine_similarity(v1, v2):
    dot = np.dot(v1, v2)
    normv1 = np.linalg.norm(v1)
    normv2 = np.linalg.norm(v2)
    cos = dot / (normv1 * normv2)
    return cos

# http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
# Cosine similarity between sentence_vectors (cosine similarity: 1 - cosine distance)
for i in range(n):
  for j in range(n):
    if i != j:
      S[i][j] = cosine_similarity(sentence_vectors[i], sentence_vectors[j])

# Pagerank Algorithm
# https://networkx.github.io/documentation/networkx-1.9.1/overview.html
G = nx.from_numpy_array(S)
scores = nx.pagerank(G)

# Tuples of the score and the sentence
list = []
for index, sentence in enumerate(sentences):
    list.append((scores[index], sentence))

df = pd.DataFrame(list, columns =['Score', 'Sentence'])
print(df.nlargest(10, 'Score'))
