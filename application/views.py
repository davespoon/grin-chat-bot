import json
import os

from dependency_injector.wiring import Provide, inject, Provider
from flask import render_template, request, jsonify
from langchain_core.language_models import BaseChatModel
from openai import OpenAI
import constants
from containers import Container
from application.response_handler import response
from dto.ModelSettings import ModelSettings


def index():
    return render_template('index.html')


@inject
def chat(container: Container = Provide[Container]):
    human_input = request.form["msg"]
    model_settings_json = request.form.get("modelSettings")
    model_settings = ModelSettings(**json.loads(model_settings_json))

    populate_model_settings(container, model_settings)

    answer = response(human_input=human_input)
    return answer


def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = file.filename
        file.save(os.path.join(constants.DATA_PATH, filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'File upload failed'}), 500


@inject
def get_models(client: OpenAI = Provide[Container.openai_client]):
    models = client.models.list()
    model_ids = [model.id for model in models]
    return jsonify(model_ids)


def populate_model_settings(container, model_settings):
    container.config.chat_openai.model.from_value(
        model_settings.model if model_settings.model is not None else constants.DEFAULT_MODEL)
    container.config.chat_openai.temperature.from_value(
        model_settings.temperature if model_settings.temperature is not None else constants.DEFAULT_TEMP)
    container.config.chat_openai.max_tokens.from_value(
        model_settings.max_tokens if model_settings.max_tokens is not None else constants.DEFAULT_MAX_TOKENS)
    container.config.chat_openai.top_p.from_value(
        model_settings.top_p if model_settings.top_p is not None else constants.DEFAULT_TOP_P)
