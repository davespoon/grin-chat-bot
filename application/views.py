import json

from dependency_injector.wiring import Provide, inject
from flask import render_template, request, jsonify
from helpers import doc_helper, config_helper
from openai import OpenAI
from containers import Container
from application.response_handler import response
from dto.ModelSettings import ModelSettings


def index():
    return render_template('index.html')


# @inject
def chat(container: Container = Provide[Container]):
    human_input = request.form["msg"]

    model_settings = ModelSettings(**json.loads(request.form.get("modelSettings")))
    config_helper.set_model_settings(container, model_settings)

    search_method_json = request.form.get("search_method")
    search_kwargs_json = request.form.get("searchKwargs")

    search_method = json.loads(search_method_json)
    search_kwargs = json.loads(search_kwargs_json)
    config_helper.set_retriever_search(container, search_method, search_kwargs)

    answer = response(human_input=human_input)
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
