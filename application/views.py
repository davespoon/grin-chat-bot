import os

from dependency_injector.wiring import Provide, inject
from flask import render_template, request, jsonify
from langchain_core.language_models import BaseChatModel

import constants
from containers import Container
from application.response_handler import response


def index():
    return render_template('index.html')


@inject
def chat(chat_openai: BaseChatModel = Provide[Container.chat_openai]):
    human_input = request.form["msg"]
    answer = response(human_input=human_input, chat_openai=chat_openai)
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
