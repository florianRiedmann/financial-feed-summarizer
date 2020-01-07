import csv
import numpy as np
import pandas as pd
from scipy import spatial
import networkx as nx

sentences = pd.read_csv('test_data/clean_sentences.csv', header=None, squeeze=True, na_filter=False)
print(sum(sentences.isna()))
sentences = sentences.tolist()

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
for i in sentences:
    if type(i) == float:
        print(i)
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

# Similarity Matrix n x n
n = len(sentences)
S = np.zeros([n, n])

# http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
# Cosine similarity between sentence_vectors (cosine similarity: 1 - cosine distance)
for i in range(n):
  for j in range(n):
    if i != j:
      S[i][j] = 1 - spatial.distance.cosine(sentence_vectors[i], sentence_vectors[j])

print(S)

# https://networkx.github.io/documentation/networkx-1.9.1/overview.html
nx_graph = nx.from_numpy_array(S)
scores = nx.pagerank(nx_graph)

ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

for i in range(10):
  print(ranked_sentences[i][1])
