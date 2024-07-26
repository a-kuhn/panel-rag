import unittest

from src.augment_prompt import build_context, build_prompt


class TestAugmentPrompt(unittest.TestCase):

    def test_build_context_with_valid_input(self):
        context_docs = [
            {
                "section": "General",
                "question": "What is your name?",
                "text": "My name is ChatGPT.",
            },
            {
                "section": "Usage",
                "question": "How to use the API?",
                "text": "You can use the API by following the documentation.",
            },
        ]
        expected_context = (
            "Section: General\n"
            "Question: What is your name?\n"
            "Answer: My name is ChatGPT.\n\n"
            "Section: Usage\n"
            "Question: How to use the API?\n"
            "Answer: You can use the API by following the documentation."
        )
        self.assertEqual(build_context(context_docs), expected_context)

    def test_build_context_with_invalid_input_not_list(self):
        context_docs = "not a list"
        expected_output = "Error: context_docs should be a list."
        self.assertEqual(build_context(context_docs), expected_output)

    def test_build_context_with_invalid_input_not_dict(self):
        context_docs = ["not a dict"]
        expected_output = "Error: Each item in context_docs should be a dictionary."
        self.assertEqual(build_context(context_docs), expected_output)

    def test_build_context_with_missing_keys(self):
        context_docs = [{"section": "General", "question": "What is your name?"}]
        expected_output = "Error: Each dictionary should contain 'section', 'question', and 'text' keys."
        self.assertEqual(build_context(context_docs), expected_output)

    def test_build_prompt_with_valid_input(self):
        question = "What is your name?"
        context_docs = [
            {
                "section": "General",
                "question": "What is your name?",
                "text": "My name is ChatGPT.",
            }
        ]
        context = build_context(context_docs)
        expected_prompt = (
            "You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.\n"
            'Only use the facts from the CONTEXT. If the CONTEXT doesn\'t contain the answer, return "NONE"\n\n'
            f"QUESTION: {question}\n\n"
            f"CONTEXT:\n{context}"
        )
        self.assertEqual(build_prompt(question, context_docs), expected_prompt)


if __name__ == "__main__":
    unittest.main()
