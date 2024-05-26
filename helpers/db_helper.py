import os
import time
from datetime import datetime

from langchain_community.vectorstores import Chroma

import constants
from helpers import doc_helper


def create_chroma_db(chunks, embedding_model, persist_directory):
    return Chroma.from_documents(chunks, embedding_model, persist_directory=persist_directory)


def get_chroma_db(embedding_model, persist_directory):
    last_update_time = get_last_update_time(persist_directory)
    docs, modification_times = doc_helper.load_documents(constants.DATA_PATH)

    if not last_update_time or any(datetime.fromtimestamp(mtime) > last_update_time for mtime in modification_times):
        chunks = doc_helper.split_text(docs)
        vectorstore = create_chroma_db(chunks, embedding_model, persist_directory)
        update_last_update_time(persist_directory)
        return vectorstore
    else:
        return Chroma(embedding_function=embedding_model, persist_directory=persist_directory)


def update_last_update_time(persist_directory):
    timestamp_file = os.path.join(persist_directory, "last_update_time.txt")
    with open(timestamp_file, "w") as file:
        file.write(str(time.time()))


def embeddings_exist(persist_directory):
    return os.path.exists(f"{persist_directory}/chroma.sqlite3")


def get_last_update_time(persist_directory):
    timestamp_file = os.path.join(persist_directory, "last_update_time.txt")
    if os.path.exists(timestamp_file):
        with open(timestamp_file, "r") as file:
            timestamp = file.read()
            return datetime.fromtimestamp(float(timestamp))
    else:
        return None
