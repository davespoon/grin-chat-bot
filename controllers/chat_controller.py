from flask import Blueprint, render_template, request
from openai import OpenAI

from dotenv import load_dotenv

from language_models.open_ai.OpenAIHandler import OpenAIHandler

load_dotenv()

chat_controller = Blueprint("chat_controller", __name__)
client = OpenAI()

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]


@chat_controller.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        content = request.form["message"]
        chat_history.append({"role": "user", "content": content})
        assistant_response_content = OpenAIHandler.get_assistant_response(chat_history)
        chat_history.append({"role": "assistant", "content": assistant_response_content})
    return render_template("index.html", chat_history=chat_history)
