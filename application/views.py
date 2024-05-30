import json

from dependency_injector.wiring import Provide, inject
from flask import render_template, request, jsonify
from langchain_openai.chat_models.base import BaseChatOpenAI
from openai import OpenAI

from application.response_handler import response
from containers import Container
from dto.ModelSettings import ModelSettings
from helpers import doc_helper, config_helper


def index():
    return render_template('index.html')


@inject
def chat(
        container: Container = Provide[Container],
        model: BaseChatOpenAI = Provide[Container.chat_openai]
):
    human_input = request.form["msg"]

    model_settings = ModelSettings(**json.loads(request.form.get("modelSettings")))
    updated_model = config_helper.set_model_settings(model, model_settings)

    search_method_json = request.form.get("search_method")
    search_kwargs_json = request.form.get("searchKwargs")

    search_method = json.loads(search_method_json)
    search_kwargs = json.loads(search_kwargs_json)
    config_helper.set_retriever_search(container, search_method, search_kwargs)

    answer = response(model=updated_model, human_input=human_input)
    return answer


def upload_file():
    file = request.files['file']
    filename = doc_helper.save_file(file)

    if filename:
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'File upload failed'}), 500


@inject
def get_models(client: OpenAI = Provide[Container.openai_client]):
    models = client.models.list()
    model_ids = [model.id for model in models]
    return jsonify(model_ids)
