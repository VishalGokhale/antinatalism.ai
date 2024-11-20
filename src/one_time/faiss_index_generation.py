import numpy as np
import pickle

import faiss


def load_embeddings():
    with open("embeddings.pkl", 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings


def create_faiss_index(embeddings):
    vector_dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    index.add(embeddings)
    faiss.write_index(index, "index.faiss")


if __name__ == '__main__':
    embeddings_ = load_embeddings()
    embeddings__ = np.array(embeddings_)
    create_faiss_index(embeddings__)
