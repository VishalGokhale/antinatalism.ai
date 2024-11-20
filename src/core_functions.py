import os

import pandas as pd

from prompt import system_prompt, user_prompt
from retrieve_from_index import load_chunks, load_index, search_user_query
from vector_db_interface import fetch_matches

from openai.lib.azure import AzureOpenAI

GPT4_O_KEY = os.getenv("GPT4_O_KEY")
GPT4_O_ENDPOINT = os.getenv("GPT4_O_ENDPOINT")
GPT4_O_API_VERSION = os.getenv("GPT4_O_API_VERSION")
GPT4_O_DEPLOYMENT = os.getenv("GPT4_O_DEPLOYMENT")


def retrieve_match_texts(matches):
    return "None"


def generate_query_for_llm(match_texts, user_query, chat_history):
    user_prompt_ = user_prompt.format(snippet1=match_texts[0], snippet2=match_texts[1], snippet3=match_texts[2],
                                      snippet4=match_texts[3], snippet5=match_texts[4], user_query=user_query)

    prompt = [
        dict(role="system", content=system_prompt),
        dict(role="user", content=user_prompt_)
    ]

    model = AzureOpenAI(
        api_key=GPT4_O_KEY,
        api_version=GPT4_O_API_VERSION,
        azure_endpoint=GPT4_O_ENDPOINT,
    )

    completion = model.chat.completions.create(model=GPT4_O_DEPLOYMENT, messages=prompt, temperature=0, seed=24)
    completion_text = completion.choices[0].message.content

    return completion_text


def get_llm_response(llm_query):
    return "This is an LLM Generated - David Benatar's response for your query"


def generate_david_response(query_for_david, chat_history):
    df = load_chunks()
    index_ = load_index()
    results_ = search_user_query(index_, query_for_david)
    merge = pd.merge(df, results_, left_index=True, right_on="ann")
    snippets = list(merge['chunks'])
    print(f"{snippets=}")
    llm_query = generate_query_for_llm(snippets, query_for_david, chat_history)
    # llm_response = get_llm_response(llm_query)

    return llm_query
