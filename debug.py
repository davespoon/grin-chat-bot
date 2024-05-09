from langchain_openai import OpenAIEmbeddings
from helpers.db_helper import create_chroma_db
from helpers.document_helper import load_documents, split_text

if __name__ == '__main__':
    documents = load_documents("data")
    chunks = split_text(documents)
    create_chroma_db(chunks, OpenAIEmbeddings())
