from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatytt.chains import ConversationalQAChain
from chatytt.vector_store.pinecone_db import PineconeDB
from server.chat_utils import parse_chat_history

load_dotenv()

app = Flask(__name__)
CORS(app)

pinecone_db = PineconeDB(index_name="youtube-transcripts", embedding_source="open-ai")
chain = ConversationalQAChain(vector_store=pinecone_db.vector_store)


@app.route("/get-answer/", methods=["POST"])
def get_answer():
    if request.method == "POST":
        data = request.get_json()
        query = data["query"]
        raw_chat_history = data["chatHistory"]

    chat_history = parse_chat_history(raw_chat_history)
    app.logger.debug(f"Query: {query}")
    app.logger.debug(f"Raw chat history: {raw_chat_history}")
    app.logger.debug(f"Parsed chat history: {chat_history}")
    response = chain.get_response(query=query, context=chat_history)

    # response = (
    #     "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent viverra, nunc et cursus iaculis, lectus"
    #     " orci ornare dui, sed euismod eros massa at purus."
    # )
    # import time
    #
    # time.sleep(1)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
