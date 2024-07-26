import unittest
from src.augment_prompt import build_prompt, build_context


class TestBuildPromptFunctions(unittest.TestCase):

    def test_build_prompt(self):
        question = "What is the refund policy?"
        context_docs = [
            {
                "section": "Payments",
                "question": "How can I request a refund?",
                "text": "You can request a refund by contacting support within 30 days of purchase.",
            }
        ]
        expected_prompt = """
You're a course teaching assistant. Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
Only use the facts from the CONTEXT. If the CONTEXT doesn't contain the answer, return "NONE"

QUESTION: What is the refund policy?

CONTEXT:
Section: Payments

Question: How can I request a refund?

Answer: You can request a refund by contacting support within 30 days of purchase.
""".strip()
        self.assertEqual(build_prompt(question, context_docs), expected_prompt)

    def test_build_context(self):
        context_docs = [
            {
                "section": "Payments",
                "question": "How can I request a refund?",
                "text": "You can request a refund by contacting support within 30 days of purchase.",
            },
            {
                "section": "Account",
                "question": "How do I reset my password?",
                "text": "You can reset your password by clicking on 'Forgot password' at login.",
            },
        ]
        expected_context = """
Section: Payments

Question: How can I request a refund?

Answer: You can request a refund by contacting support within 30 days of purchase.

Section: Account

Question: How do I reset my password?

Answer: You can reset your password by clicking on 'Forgot password' at login.
""".strip()
        self.assertEqual(build_context(context_docs), expected_context)

    def test_build_context_invalid_docs(self):
        with self.assertRaises(ValueError):
            build_context("invalid input")
        with self.assertRaises(ValueError):
            build_context([{"section": "Payments"}])
        with self.assertRaises(ValueError):
            build_context(
                [{"section": "Payments", "question": "How can I request a refund?"}]
            )
        with self.assertRaises(ValueError):
            build_context(
                [
                    {
                        "section": "Payments",
                        "text": "You can request a refund by contacting support within 30 days of purchase.",
                    }
                ]
            )

    def test_build_context_non_dict_item(self):
        with self.assertRaises(ValueError):
            build_context(
                [
                    {
                        "section": "Payments",
                        "question": "How can I request a refund?",
                        "text": "You can request a refund by contacting support within 30 days of purchase.",
                    },
                    "invalid item",
                ]
            )


if __name__ == "__main__":
    unittest.main()
