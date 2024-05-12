import constants
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from helpers import doc_helper, db_helper

load_dotenv()

if not db_helper.embeddings_exist(constants.CHROMA_PATH):
    docs = doc_helper.load_documents(constants.DATA_PATH)
    chunks = doc_helper.split_text(docs)
    vectorstore = db_helper.create_chroma_db(chunks, OpenAIEmbeddings(), constants.CHROMA_PATH)
