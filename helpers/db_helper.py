import os

from langchain_community.vectorstores import Chroma


def create_chroma_db(chunks, embedding_model, persist_directory):
    return Chroma.from_documents(chunks, embedding_model, persist_directory=persist_directory)


def get_chroma_db(embedding_model, persist_directory):
    if embeddings_exist(persist_directory):
        return Chroma(embedding_function=embedding_model, persist_directory=persist_directory)
    else:
        raise FileNotFoundError("No Chroma db found. Try create it first.")


def embeddings_exist(persist_directory):
    return os.path.exists(f"{persist_directory}/chroma.sqlite3")
