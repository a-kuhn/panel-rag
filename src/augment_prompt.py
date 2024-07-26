def build_prompt(question: str, context_docs: list[dict]) -> str:
    context = build_context(context_docs)
    prompt = f"""
You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "NONE"

QUESTION: {question}

CONTEXT:
{context}
""".strip()
    return prompt


def build_context(context_docs: list[dict]) -> str:
    if not isinstance(context_docs, list):
        raise ValueError("context_docs should be a list.")

    context_lines = []

    for doc in context_docs:
        if not isinstance(doc, dict):
            raise ValueError("Each item in context_docs should be a dictionary.")
        if not all(key in doc for key in ["section", "question", "text"]):
            raise ValueError(
                "Each dictionary should contain 'section', 'question', and 'text' keys."
            )

        context_lines.append(f"Section: {doc['section']}")
        context_lines.append(f"Question: {doc['question']}")
        context_lines.append(f"Answer: {doc['text']}")

    return "\n\n".join(context_lines)
