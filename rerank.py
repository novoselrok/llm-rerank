import re
from typing import Tuple, List, Dict, Any

import llms

model = llms.init("gpt-3.5-turbo")

reranking_prompt = """A list of documents is shown below. Each document has a number next to it along with a summary of the document. A question is also provided. Respond with the numbers of the documents you should consult to answer the question, in order of relevance. Do not include any documents that are not relevant to the question.
Example format:
Document 1:
<summary of document 1>
Document 2:
<summary of document 2>
...
Document 10:
<summary of document 10>
Question: <question>
Answer:
Document 9
Document 3
Document 7
Let's try this now:
{context}
Question: {question}
Answer:
"""


def parse_rerank_input(input: str) -> Tuple[str, List[Dict[str, str]]]:
    lines = [line.strip() for line in input.split("\n") if len(line.strip()) > 0]
    query = lines[0]
    documents = []
    for line in lines[1:]:
        columns = [column.strip() for column in line.split(",")]
        documents.append(
            {"title": columns[0], "url": columns[1], "snippet": ", ".join(columns[2:])}
        )
    return query, documents


DOCUMENT_NUMBER_REGEXP = re.compile(r"document:?\s+(\d+)")


def parse_model_completion(completion: str) -> List[int]:
    sections = completion.lower().split("answer:")
    answer_section = sections[-1]
    document_lines = [
        line.strip() for line in answer_section.split("\n") if len(line.strip()) > 0
    ]

    document_numbers = []
    for line in document_lines:
        match = DOCUMENT_NUMBER_REGEXP.search(line)
        if match is None:
            # Invalid answer format.
            continue
        document_numbers.append(int(match.group(1)))
    return document_numbers


def document_to_prompt_example(idx: int, document: Dict[str, str]) -> str:
    return f"Document {idx+1}:\n{document['title']} ({document['url']}): {document['snippet']}"


def get_relevant_reranked_documents(
    query: str, documents: List[Dict[str, str]]
) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    context = "\n".join(
        [
            document_to_prompt_example(idx, result)
            for idx, result in enumerate(documents)
        ]
    )
    prompt = reranking_prompt.replace("{context}", context).replace("{question}", query)
    result = model.complete(prompt, temperature=0, max_tokens=300)

    return [
        documents[document_number - 1]
        for document_number in parse_model_completion(result.text)
    ], result.meta
