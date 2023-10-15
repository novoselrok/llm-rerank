from flask import Flask, render_template, request

from rerank import get_relevant_reranked_documents, parse_rerank_input

app = Flask(__name__, static_url_path="/llm-rerank/static")


@app.route("/llm-rerank")
def index():
    return render_template("index.html")


@app.route("/llm-rerank/api/rerank", methods=["POST"])
def query():
    body = request.json
    query, documents = parse_rerank_input(body["input"])
    reranked_documents, rerank_metadata = get_relevant_reranked_documents(
        query, documents
    )
    return {"documents": reranked_documents, "metadata": rerank_metadata}
