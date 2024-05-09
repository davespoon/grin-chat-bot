import os.path
import shutil
import constants

from langchain_community.vectorstores import Chroma


def create_chroma_db(chunks, embedding_model, persist_directory=constants.CHROMA_PATH):
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    db = Chroma.from_documents(chunks, embedding_model, persist_directory)
    db.persist()
    return db
