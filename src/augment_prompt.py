def build_prompt(question: str, context_docs: list) -> str:
    context = build_context(context_docs)
    prompt = f"""
You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "NONE"

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    return prompt


def build_context(context_docs: list) -> str:
    context = ""

    if not isinstance(context_docs, list):
        return "Error: context_docs should be a list."

    for doc in context_docs:
        if not isinstance(doc, dict):
            return "Error: Each item in context_docs should be a dictionary."

        if not all(key in doc for key in ["section", "question", "text"]):
            return "Error: Each dictionary should contain 'section', 'question', and 'text' keys."

        context += f"Section: {doc['section']}\n"
        context += f"Question: {doc['question']}\n"
        context += f"Answer: {doc['text']}\n\n"

    return context.strip()
