import json

from dependency_injector.wiring import Provide, inject
from flask import render_template, request, jsonify
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever
from openai import OpenAI

import constants
from application.response_handler import response
from containers import Container
from helpers import doc_helper, config_helper
from models.ModelSettings import ModelSettings
from repositories.ProfileRepository import ProfileRepository


def index():
    return render_template('index.html')


@inject
def chat(
        retriever: VectorStoreRetriever = Provide[Container.retriever],
        model: BaseChatModel = Provide[Container.chat_openai]
):
    human_input = request.form["msg"]

    model_settings = ModelSettings(**json.loads(request.form.get("modelSettings")))
    updated_model = config_helper.set_model_settings(model, model_settings)

    search_method_json = request.form.get("search_method")
    search_kwargs_json = request.form.get("searchKwargs")

    search_method = json.loads(search_method_json)
    search_kwargs = json.loads(search_kwargs_json)
    configured_retriever = config_helper.set_retriever_search(retriever, search_method, search_kwargs)

    answer = response(model=updated_model, retriever=configured_retriever, human_input=human_input)
    return answer


def upload_file():
    file = request.files['file']
    filename = doc_helper.save_file(file)
    docs, modification_times = doc_helper.load_documents(constants.DATA_PATH)
    extracted_text = doc_helper.extract_resume_info(docs)
    repo = ProfileRepository("profiles.db")
    profile_id = repo.add_profile(extracted_text)

    if filename:
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    return jsonify({'error': 'File upload failed'}), 500


@inject
def get_models(client: OpenAI = Provide[Container.openai_client]):
    models = client.models.list()
    model_ids = [model.id for model in models]
    return jsonify(model_ids)
