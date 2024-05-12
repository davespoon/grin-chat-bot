from flask import Flask, render_template, request
from langchain_core.messages import HumanMessage

from response_handler import response

app = Flask(__name__)
chat_history = ["You are polite and helpful assistant"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    human_input = request.form["msg"]
    ai_msg = response(human_input=human_input, chat_history=chat_history)
    # chat_history.extend([HumanMessage(content=human_input), ai_msg["answer"]])

    return ai_msg["answer"]


if __name__ == '__main__':
    app.run()
