from language_models.open_ai.OpenAICommunicator import OpenAICommunicator


class OpenAIHandler:
    @staticmethod
    def get_assistant_response(chat_history, openai_client=None):
        return OpenAICommunicator(openai_client).get_response(chat_history)
