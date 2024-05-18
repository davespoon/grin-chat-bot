from dependency_injector import containers, providers
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from helpers.db_helper import get_chroma_db


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        packages=[
            "application"
        ],
    )

    chat_openai = providers.Singleton(
        ChatOpenAI,
        model="gpt-3.5-turbo",
        temperature=0,
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
