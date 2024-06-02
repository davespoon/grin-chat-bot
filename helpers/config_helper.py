from typing import Any, Dict

from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever


def set_model_settings(model: BaseChatModel, model_settings):
    model.model_name = model_settings.model
    model.temperature = float(model_settings.temperature)
    model.max_tokens = int(model_settings.max_tokens)
    model.model_kwargs = {"top_p": model_settings.top_p}
    return model


def set_retriever_search(retriever: VectorStoreRetriever, search_method, search_kwargs):
    retriever.search_type = search_method
    retriever.search_kwargs = parse_dict(search_kwargs)
    return retriever
    # container.config.retriever.search_method.from_value(search_method)
    # container.config.retriever.search_kwargs.from_value(search_kwargs)


def parse_dict(args: Dict[str, str]) -> Dict[str, Any]:
    return {key: convert_value(value) for key, value in args.items()}


def convert_value(value: str) -> Any:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
