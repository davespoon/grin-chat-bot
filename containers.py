from dependency_injector import containers, providers
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI

import constants
from helpers.db_helper import get_chroma_db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        packages=[
            "application"
        ],
    )

    openai_client = providers.Singleton(
        OpenAI,
        api_key=config.api_key
    )

    chat_openai = providers.Singleton(
        ChatOpenAI,
        model=constants.LLM_DEFAULT_MODEL,
        temperature=constants.DEFAULT_TEMP,
        max_tokens=constants.DEFAULT_MAX_TOKENS,
        top_p=constants.DEFAULT_TOP_P,
        openai_api_key=config.api_key
    )

    openai_embeddings = providers.Factory(
        OpenAIEmbeddings,
        openai_api_key=config.api_key,
        model=constants.EMBEDDING_DEFAULT_MODEL

    )

    chroma_db = providers.Factory(
        get_chroma_db,
        embedding_model=openai_embeddings,
        persist_directory=config.chroma.persist_directory
    )

    retriever = providers.Factory(
        VectorStoreRetriever,
        vectorstore=chroma_db,
        search_type="similarity"
    )
