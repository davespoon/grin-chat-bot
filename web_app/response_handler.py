import os
import bs4
import getpass

import openai
from langchain import hub
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langsmith import Client

import constants
from helpers import doc_helper, db_helper
from templates import prompts


def response(user_query):
    load_dotenv()
    langchain_client = Client
    openai_api_key = os.getenv("OPENAI_API_KEY")

    docs = doc_helper.load_documents(constants.DATA_PATH)

    chunks = doc_helper.split_text(docs)
    vectorstore = db_helper.get_chroma_db(chunks, OpenAIEmbeddings(), constants.CHROMA_PATH)

    # Retrieve info from chosen source
    retriever = vectorstore.as_retriever(search_type="similarity")
    # prompt = hub.pull("rlm/rag-prompt")

    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    template = prompts.base_template

    # Add the context to your user query
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {"context": retriever
             # | format_docs,
                , "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )

    return chain.invoke(user_query)
