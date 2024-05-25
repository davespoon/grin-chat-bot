from dependency_injector import containers, providers
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
        model=constants.MODEL,
        temperature=constants.TEMPERATURE,

        openai_api_key=config.api_key
    )

    openai_embeddings = providers.Factory(
        OpenAIEmbeddings,
        openai_api_key=config.api_key
    )

    chroma_db = providers.Factory(
        get_chroma_db,
        embedding_model=openai_embeddings,
        persist_directory=config.persist_directory
    )
