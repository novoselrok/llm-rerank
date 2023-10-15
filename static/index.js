function renderResponse({ documents, metadata }) {
  const documentsSection = documents
    .map(
      (document) => `${document.title}\n${document.url}\n${document.snippet}`
    )
    .join("\n\n");

  const metadataSection = [
    `Latency: ${metadata.latency} seconds`,
    `Tokens in/out: ${metadata.tokens_prompt}/${metadata.tokens_completion}`,
    `Cost: $${metadata.cost} USD`,
  ].join("\n");

  return `${documentsSection}\n\n${metadataSection}`;
}

function onLoad() {
  const input = document.querySelector(".query-input");
  const submitButton = document.querySelector(".submit-button");
  const answerSection = document.querySelector(".answer");
  const answerSkeleton = document.querySelector(".answer-skeleton");
  const answerContent = document.querySelector(".answer-content");

  const onSubmit = async () => {
    answerSection.style.display = "block";
    answerSkeleton.style.display = "block";
    answerContent.innerText = "";

    const response = await fetch("/llm-rerank/api/rerank", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: input.value }),
    }).then((response) => response.json());

    answerSkeleton.style.display = "none";
    answerContent.innerText = renderResponse(response);
  };

  submitButton.addEventListener("click", onSubmit);
}

document.addEventListener("DOMContentLoaded", onLoad);
