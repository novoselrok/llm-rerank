import argparse
import glob
from typing import Optional

from rerank import parse_rerank_input, get_relevant_reranked_documents


def evaluate(test_file_filter: Optional[str] = None):
    test_files = glob.glob("testdata/*.txt")
    for test_file in test_files:
        if test_file_filter is not None and test_file_filter not in test_file:
            continue

        with open(test_file, encoding="utf-8") as f:
            file_content = f.read()

        query, documents = parse_rerank_input(file_content)
        reranked_documents, rerank_metadata = get_relevant_reranked_documents(
            query, documents
        )

        print("File:", test_file)
        print("Query:", query, "\n")
        for document in reranked_documents:
            print(document["title"])
            print(document["url"])
            print(document["snippet"])
            print()

        print(f"Latency: {rerank_metadata['latency']}s")
        print(
            f"Tokens in/out: {rerank_metadata['tokens_prompt']}/{rerank_metadata['tokens_completion']}"
        )
        print(f"Cost: ${rerank_metadata['cost']} USD")
        print("*" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", dest="filter", required=False)
    args = parser.parse_args()
    evaluate(args.filter)
