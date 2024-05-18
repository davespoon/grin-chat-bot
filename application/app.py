from dotenv import load_dotenv
from flask import Flask

import constants
from application import views
from containers import Container


def flask_app() -> Flask:
    container = Container()
    container.config.api_key.from_env("OPENAI_API_KEY")
    container.config.persist_directory.from_value(constants.CHROMA_PATH)

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index, methods=['GET'])
    app.add_url_rule("/chat", "chat", views.chat, methods=['GET', 'POST'])
    return app


if __name__ == "__main__":
    load_dotenv()
    flask_app().run()
