# LLM Rerank

LLM Rerank is an app that allows reranking a list of potential results based on the user context or query.

## Usage Instructions

Step 1: Install the dependencies

```bash
pip3 install -r requirements.txt
```

Step 2: Launch the app

```bash
export OPENAI_API_KEY="..."
flask --app app run --port 5001
```

Step 3: (Optional) Offline evaluation

```bash
python3 evaluate.py
```

## Future Improvements

The LLMs allow us to quickly prompt engineer features like reranking a set of search results. But that comes at a considerable cost in terms of cost and latency.

We could alleviate those concerns by using a lightweight cross-encoder model. The cross-encoder model outputs a similarity score for a particular query and a document. The key benefit of the cross-encoder model is that it attends to the query and document tokens jointly, allowing it to learn complex interactions between the two. Additionally, cross-encoder models are typically much smaller than generative models so they can perform inference much faster, reducing latency and cost. Furthermore, we could fine-tune the cross-encoder model on a dataset of queries and relevant documents we care about in our system (e.g, programming questions and code snippets from StackOverflow), improving the overall relevance of results for our users.
