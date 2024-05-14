from flask import Flask

from application import views
from containers import Container


def flask_app() -> Flask:
    container = Container()
    container.config.api_key.from_env("OPENAI_API_KEY")

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index, methods=['GET'])
    app.add_url_rule("/chat", "chat", views.chat, methods=['GET', 'POST'])
    # container.wire(modules=[__name__])
    return app
