import constants


def model_settings(container, model_settings):
    container.config.chat_openai.model.from_value(
        model_settings.model if model_settings.model is not None else constants.DEFAULT_MODEL)
    container.config.chat_openai.temperature.from_value(
        model_settings.temperature if model_settings.temperature is not None else constants.DEFAULT_TEMP)
    container.config.chat_openai.max_tokens.from_value(
        model_settings.max_tokens if model_settings.max_tokens is not None else constants.DEFAULT_MAX_TOKENS)
    container.config.chat_openai.top_p.from_value(
        model_settings.top_p if model_settings.top_p is not None else constants.DEFAULT_TOP_P)


def retriever_search(container, kwargs):
    container.config.retriever.search_kwargs = kwargs
