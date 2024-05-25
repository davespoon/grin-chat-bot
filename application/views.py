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


# @inject
def chat():
    human_input = request.form["msg"]
    model_settings_json = request.form.get("modelSettings")
    model_settings = ModelSettings(**json.loads(model_settings_json))

    answer = response(human_input=human_input, model_settings=model_settings)
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
