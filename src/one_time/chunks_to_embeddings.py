import os
import pickle

from dotenv import load_dotenv
from openai.lib.azure import AzureOpenAI

load_dotenv()
EMBEDDING_KEY = os.getenv("EMBEDDING_KEY")
EMBEDDING_API_VERSION = os.getenv("EMBEDDING_API_VERSION")
EMBEDDING_ENDPOINT = os.getenv("EMBEDDING_ENDPOINT")
EMBEDDING_DEPLOYMENT = os.getenv("EMBEDDING_DEPLOYMENT")


def load_chunks():
    with open(r"C:\Users\gokhvis\Documents\antinatalism.ai\src\chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return chunks


def chunks_to_embeddings(chunks):
    model = AzureOpenAI(
        api_key=EMBEDDING_KEY,
        api_version=EMBEDDING_API_VERSION,
        azure_endpoint=EMBEDDING_ENDPOINT,
    )
    embeddings = []
    chunk_count = len(chunks)
    for i in range(0, chunk_count, 64):
        chunk_set = chunks[i:i + 64]
        emb = model.embeddings.create(input=chunk_set, model=EMBEDDING_DEPLOYMENT)
        embeddings.extend([e.embedding for e in emb.data])

    return embeddings


def single_chunk_to_embedding(chunk):
    model = AzureOpenAI(
        api_key=EMBEDDING_KEY,
        api_version=EMBEDDING_API_VERSION,
        azure_endpoint=EMBEDDING_ENDPOINT,
    )
    emb = model.embeddings.create(input=[chunk], model=EMBEDDING_DEPLOYMENT)
    return emb.data[0].embedding


def save_embeddings(embeddings):
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)


if __name__ == '__main__':
    chunks_ = load_chunks()
    embeddings_ = chunks_to_embeddings(chunks_)
    save_embeddings(embeddings_)
