from langchain_community.vectorstores import Chroma


def get_chroma_db(chunks, embedding_model, persist_directory):
    db = Chroma.from_documents(chunks, embedding_model, persist_directory=persist_directory)
    return db
