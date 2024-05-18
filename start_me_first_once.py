from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from helpers import doc_helper, db_helper
import constants

load_dotenv()

docs = doc_helper.load_documents(constants.DATA_PATH)
chunks = doc_helper.split_text(docs)
vectorstore = db_helper.create_chroma_db(chunks, OpenAIEmbeddings(), constants.CHROMA_PATH)
