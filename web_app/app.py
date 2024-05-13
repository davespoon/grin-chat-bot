from flask import Flask, render_template, request
from langchain_core.messages import HumanMessage

from response_handler import response

app = Flask(__name__)


# chat_history = ["You are polite and helpful assistant"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    human_input = request.form["msg"]
    answer = response(human_input=human_input)
    return answer


if __name__ == '__main__':
    app.run()
