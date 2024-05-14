from dependency_injector import containers, providers
from langchain_openai import ChatOpenAI


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(
        packages=[
            "application",
        ],
    )

    chat_openai = providers.Singleton(
        ChatOpenAI,
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=config.api_key
    )

    # chroma_db = providers.Factory(
    #     get_chroma_db,
    #     embedding_model,
    #     config.persist_directory,
    #
    # )
    #
    # openai_embeddings = providers.Dependency(
    #
    # )
