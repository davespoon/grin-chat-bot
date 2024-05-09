from dotenv import load_dotenv
from flask import (render_template, request, Response, stream_with_context, jsonify, Blueprint)
from openai import OpenAI

load_dotenv()

chat_controller = Blueprint("chat_controller", __name__)
client = OpenAI()

chat_history = [{"role": "system", "content": "You are a helpful assistant."}]


@chat_controller.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)


@chat_controller.route("/chat", methods=["POST"])
def chat():
    content = request.json["message"]
    chat_history.append({"role": "user", "content": content})
    return jsonify(success=True)


@chat_controller.route("/stream", methods=["GET"])
def stream():
    def generate():
        assistant_response_content = ""

        with client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history,
                stream=True,
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    # Accumulate the content only if it's not None
                    assistant_response_content += chunk.choices[0].delta.content
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
                if chunk.choices[0].finish_reason == "stop":
                    break  # Stop if the finish reason is 'stop'

        # Once the loop is done, append the full message to chat_history
        chat_history.append(
            {"role": "assistant", "content": assistant_response_content}
        )

    return Response(stream_with_context(generate()), mimetype="text/event-stream")
