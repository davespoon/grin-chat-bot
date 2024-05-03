class OpenAICommunicator:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def get_response(self, chat_history):
        assistant_response_content = ""
        with self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history,
                stream=False,  # Changed to False for synchronous response
        ) as response:
            assistant_response_content = response.choices[0].message.content
        return assistant_response_content
