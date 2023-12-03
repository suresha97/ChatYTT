from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatytt.chains.standard.qa_chain import QAChain
from chatytt.vector_store.pinecone_db import PineconeDB

load_dotenv()

app = Flask(__name__)
CORS(app)

pinecone_db = PineconeDB(index_name="youtube-transcripts", embedding_source="open-ai")
qa_chain = QAChain()


@app.route("/get-answer/", methods=["GET", "POST"])
def get_answer():
    if request.method == "GET":
        query = request.args.get("query")
    if request.method == "POST":
        data = request.get_json()
        query = data["query"]

    similar_docs = pinecone_db.get_similar_docs(query=query, top_k=5)
    response = qa_chain.get_response(query=query, context=similar_docs)

    # response = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent viverra, nunc et cursus iaculis, lectus" \
    #            " orci ornare dui, sed euismod eros massa at purus. Sed hendrerit metus neque, sed porta purus consequat non. " \
    #            "Aliquam blandit nibh at nibh efficitur posuere. Nunc ultricies urna eget dolor imperdiet ullamcorper. Duis dolor " \
    #            "ante, congue et pellentesque vitae, imperdiet eleifend nisl. Donec sed nisl vel ex bibendum mattis. Sed facilisis " \
    #            "vitae arcu vitae elementum. Ut sed semper leo. Donec convallis orci in metus interdum, nec pulvinar risus semper."
    # import time
    # time.sleep(1)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True, port=8080)
