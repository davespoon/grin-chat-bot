from dependency_injector.wiring import Provide, inject
from flask import render_template, request
from langchain_core.language_models import BaseChatModel

from containers import Container
from application.response_handler import response


@inject
def index():
    return render_template('index.html')


@inject
def chat(chat_openai: BaseChatModel = Provide[Container.chat_openai]):
    human_input = request.form["msg"]
    answer = response(human_input=human_input, chat_openai=chat_openai)
    return answer
