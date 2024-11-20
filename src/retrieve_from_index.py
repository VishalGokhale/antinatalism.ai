from functools import lru_cache

import faiss
import numpy as np
import pandas as pd

from one_time.chunks_to_embeddings import single_chunk_to_embedding


@lru_cache
def load_index():
    index = faiss.read_index(r"C:\Users\gokhvis\Documents\antinatalism.ai\src\one_time\index.faiss")
    print(f"Loaded index    ....    ....    ... .. {index.ntotal=}")
    return index


def search_user_query(index, single_chunk):
    query_embedding = single_chunk_to_embedding(single_chunk)
    query_embedding = np.array([query_embedding])
    distances, ann = index.search(query_embedding, 5)
    print(f"{distances=}")
    print(f"{ann=}")
    results = pd.DataFrame({"distance": distances[0], "ann": ann[0]})
    print(results)
    return results


@lru_cache()
def load_chunks():
    df = pd.read_excel(r"C:\Users\gokhvis\Documents\antinatalism.ai\src\chunks.xlsx")
    return df


if __name__ == '__main__':
    single_chunk_ = "The world is a terrible place"
    df = load_chunks()
    index_ = load_index()
    results_ = search_user_query(index_, single_chunk_)
    merge = pd.merge(df, results_, left_index=True, right_on="ann")
    merge.to_excel(r"C:\Users\gokhvis\Documents\antinatalism.ai\src\merge.xlsx")
    print(merge)
