import os
from flask import Flask
from controllers.chat_controller import chat_controller
from controllers.reset_controller import reset_controller

app = Flask(__name__)
app.register_blueprint(chat_controller)
app.register_blueprint(reset_controller)

if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
