from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatytt.chains.standard import ConversationalQAChain
from chatytt.vector_store.pinecone_db import PineconeDB
from server.utils.chat import parse_chat_history
from server.utils.dynamodb import (
    is_new_user,
    fetch_chat_history,
    create_chat_history,
    update_chat_history,
)

load_dotenv()

app = Flask(__name__)
CORS(app)

pinecone_db = PineconeDB(index_name="youtube-transcripts", embedding_source="open-ai")
chain = ConversationalQAChain(vector_store=pinecone_db.vector_store)


@app.route("/get-query-response/", methods=["POST"])
def get_query_response():
    if request.method == "POST":
        data = request.get_json()
        query = data["query"]
        raw_chat_history = data["chatHistory"]

    chat_history = parse_chat_history(raw_chat_history)

    app.logger.debug(f"Query: {query}")
    app.logger.debug(f"Raw chat history: {raw_chat_history}")
    app.logger.debug(f"Parsed chat history: {chat_history}")

    response = chain.get_response(query=query, chat_history=chat_history)

    return jsonify({"response": response})


@app.route("/get-chat-history/", methods=["GET"])
def get_chat_history():
    user_id = request.args.get("userId")
    app.logger.debug(f"userid: {user_id}")

    if is_new_user(user_id):
        response = {"chatHistory": []}
        app.logger.debug(f"response: {response}")
        return jsonify({"response": response})

    response = {"chatHistory": fetch_chat_history(user_id=user_id)["ChatHistory"]}
    app.logger.debug(f"response: {response}")

    return jsonify({"response": response})


@app.route("/save-chat-history/", methods=["PUT"])
def save_chat_history():
    app.logger.debug(f"request: {request.get_json()}")
    data = request.get_json()
    user_id = data["userId"]

    if is_new_user(user_id):
        create_chat_history(user_id=user_id, chat_history=data["chatHistory"])
    else:
        update_chat_history(user_id=user_id, chat_history=data["chatHistory"])

    return jsonify({"response": "chat saved"})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
