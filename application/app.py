import uuid

from dotenv import load_dotenv
from flask import Flask

import constants
from application.controllers import chat, profiles
from containers import Container
from repositories import db


def flask_app() -> Flask:
    container = Container()
    container.config.api_key.from_env("OPENAI_API_KEY")
    container.config.chroma.persist_directory.from_value(constants.CHROMA_PATH)

    app = Flask(__name__)
    app.container = container
    app.secret_key = "key"
    app.add_url_rule("/", "index", chat.index, methods=['GET'])
    app.add_url_rule("/chat", "chat", chat.chat, methods=['GET', 'POST'])
    app.add_url_rule("/upload", "upload", chat.upload_file, methods=['POST'])
    app.add_url_rule("/models", "models", chat.get_models, methods=['GET'])

    app.add_url_rule("/profiles", "profiles", profiles.index, methods=['GET'])
    app.add_url_rule("/profiles/upload", "upload_profile", profiles.upload_profile, methods=['POST'])
    app.add_url_rule("/profiles/<int:profile_id>/delete", "delete_profile", profiles.delete_profile, methods=['POST'])
    # app.add_url_rule("/profiles/<int:profile_id>/edit", "edit_profile", profiles.edit_profile, methods=['GET'])
    # app.add_url_rule("/profiles/<int:profile_id>/update", "update_profile", profiles.update_profile, methods=['POST'])
    return app


if __name__ == "__main__":
    load_dotenv()
    db.init_db()
    flask_app().run()
