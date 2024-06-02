from langchain_core.language_models import BaseChatModel


def set_model_settings(model: BaseChatModel, model_settings):
    model.model_name = model_settings.model
    model.temperature = float(model_settings.temperature)
    model.max_tokens = int(model_settings.max_tokens)
    model.model_kwargs = {"top_p": model_settings.top_p}
    return model


def set_retriever_search(container, search_method, search_kwargs):
    container.config.retriever.search_method.from_value(search_method)
    container.config.retriever.search_kwargs.from_value(search_kwargs)
