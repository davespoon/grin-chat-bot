import os

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import constants
from helpers import doc_helper


def create_chroma_db(chunks, embedding_model, persist_directory):
    return Chroma.from_documents(chunks, embedding_model, persist_directory=persist_directory)


def get_chroma_db(embedding_model, persist_directory):
    if embeddings_exist(persist_directory):
        return Chroma(embedding_function=embedding_model, persist_directory=persist_directory)
    else:
        docs = doc_helper.load_documents(constants.DATA_PATH)
        chunks = doc_helper.split_text(docs)
        vectorstore = create_chroma_db(chunks, embedding_model, persist_directory)
        return vectorstore


def embeddings_exist(persist_directory):
    return os.path.exists(f"{persist_directory}/chroma.sqlite3")
