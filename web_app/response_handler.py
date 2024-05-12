import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langsmith import Client

import constants
from helpers import db_helper
from prompts import prompt_templates


def response(user_query):
    load_dotenv()
    langchain_client = Client
    openai_api_key = os.getenv("OPENAI_API_KEY")

    vectorstore = db_helper.get_chroma_db(OpenAIEmbeddings(), constants.CHROMA_PATH)

    retriever = vectorstore.as_retriever(search_type="similarity")
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
    template = prompt_templates.base_template
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )

    return chain.invoke(user_query)
