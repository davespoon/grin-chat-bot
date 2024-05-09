import os
import bs4
import getpass
from langchain import hub
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

import constants
from helpers import doc_helper, db_helper
from prompt_templates import prompts


def response(user_query):
    # Load environment and get your openAI api key
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    docs = doc_helper.load_pdf("data/VideoGamesHistory.pdf")

    chunks = doc_helper.split_text(docs)
    vectorstore = db_helper.get_chroma_db(chunks, OpenAIEmbeddings(), constants.CHROMA_PATH)

    # Retrieve info from chosen source
    retriever = vectorstore.as_retriever(search_type="similarity")
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    template = prompts.base_template

    # Add the context to your user query
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | custom_rag_prompt
            | llm
            | StrOutputParser()
    )

    return rag_chain.invoke(user_query)
