import pytest
from src.augment_prompt import build_prompt, build_context


def compare_lines(expected, actual):
    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()
    assert len(expected_lines) == len(
        actual_lines
    ), f"Number of lines in the output ({len(actual_lines)}) does not match the expected number ({len(expected_lines)})."
    for e, a in zip(expected_lines, actual_lines):
        assert e.strip() == a.strip(), f"Expected: '{e.strip()}' but got: '{a.strip()}'"


def test_build_context_valid_input():
    context_docs = [
        {
            "section": "Introduction",
            "question": "What is Python?",
            "text": "Python is a programming language.",
        },
        {
            "section": "Usage",
            "question": "How to use Python?",
            "text": "Python can be used for web development.",
        },
    ]
    expected_context = (
        "Section: Introduction\n\n"
        "Question: What is Python?\n\n"
        "Answer: Python is a programming language.\n\n"
        "Section: Usage\n\n"
        "Question: How to use Python?\n\n"
        "Answer: Python can be used for web development.\n"
    )
    compare_lines(expected_context, build_context(context_docs))


def test_build_context_invalid_type():
    with pytest.raises(ValueError, match="context_docs should be a list."):
        build_context("invalid type")


def test_build_context_invalid_item_type():
    with pytest.raises(
        ValueError, match="Each item in context_docs should be a dictionary."
    ):
        build_context(["invalid type"])


def test_build_context_missing_keys():
    context_docs = [{"section": "Introduction", "question": "What is Python?"}]
    with pytest.raises(
        ValueError,
        match="Each dictionary should contain 'section', 'question', and 'text' keys.",
    ):
        build_context(context_docs)


def test_build_prompt_valid_input():
    question = "What is Python?"
    context_docs = [
        {
            "section": "Introduction",
            "question": "What is Python?",
            "text": "Python is a programming language.",
        },
        {
            "section": "Usage",
            "question": "How to use Python?",
            "text": "Python can be used for web development.",
        },
    ]
    expected_prompt = """
You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "NONE"

QUESTION: What is Python?

CONTEXT:
Section: Introduction

Question: What is Python?

Answer: Python is a programming language.

Section: Usage

Question: How to use Python?

Answer: Python can be used for web development.
""".strip()
    assert build_prompt(question, context_docs) == expected_prompt


def test_build_prompt_empty_context():
    question = "What is Python?"
    context_docs = []
    expected_prompt = """
You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "NONE"

QUESTION: What is Python?

CONTEXT:

""".strip()
    assert build_prompt(question, context_docs) == expected_prompt
