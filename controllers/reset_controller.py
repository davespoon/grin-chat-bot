from flask import Blueprint, jsonify

reset_controller = Blueprint("reset_controller", __name__)


@reset_controller.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history: list[dict[str, str]] = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)
