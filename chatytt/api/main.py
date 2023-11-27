from flask import Flask, request
from dotenv import load_dotenv

from chatytt.chains.qa_chain import QAChain
from vector_store.pinecone_db import PineconeDB

load_dotenv()

app = Flask(__name__)

pinecone_db = PineconeDB(index_name="youtube-transcripts", embedding_source="open-ai")
qa_chain = QAChain()


@app.route("/get-answer/", methods=["GET"])
def get_answer():
    query = request.args.get("query")
    similar_docs = pinecone_db.get_similar_docs(query=query)

    response = qa_chain.get_response(query=query, context=similar_docs)

    return response


if __name__ == "__main__":
    app.run(debug=True)
