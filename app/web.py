from flask import Flask, render_template, request, jsonify
from app.chatbot import Chatbot

app = Flask(__name__)

chatbot = Chatbot()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    response = chatbot.ask(question)

    return jsonify({
        "answer": response.answer,
        "sources": response.sources
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8001,
        debug=True
    )