import unittest
from unittest.mock import patch, Mock
from src.generate_response import OllamaResponseGenerator, OpenAIResponseGenerator


class TestOllamaResponseGenerator(unittest.TestCase):
    @patch("src.generate_response.Client")
    def test_generate_response_success(self, MockClient):
        mock_client = MockClient.return_value
        mock_response = {"message": {"content": "This is a test response from Ollama."}}
        mock_client.chat.return_value = mock_response

        generator = OllamaResponseGenerator()
        prompt = "Test prompt"
        response = generator.generate_response(prompt)

        self.assertEqual(response, "This is a test response from Ollama.")
        mock_client.chat.assert_called_once_with(
            model="phi3", messages=[{"role": "user", "content": prompt}]
        )

    @patch("src.generate_response.Client")
    def test_generate_response_failure(self, MockClient):
        mock_client = MockClient.return_value
        mock_client.chat.side_effect = Exception("Test exception")

        generator = OllamaResponseGenerator()
        prompt = "Test prompt"
        response = generator.generate_response(prompt)

        self.assertEqual(response, "No response from Ollama client")


class TestOpenAIResponseGenerator(unittest.TestCase):
    @patch("src.generate_response.OpenAI")
    def test_generate_response_success(self, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = (
            "This is a test response from OpenAI."
        )

        mock_client.chat.completions.create.return_value = mock_response

        generator = OpenAIResponseGenerator(api_key="test_key")
        prompt = "Test prompt"
        response = generator.generate_response(prompt)

        self.assertEqual(response, "This is a test response from OpenAI.")
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o", messages=[{"role": "user", "content": prompt}]
        )

    @patch("src.generate_response.OpenAI")
    def test_generate_response_failure(self, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.side_effect = Exception("Test exception")

        generator = OpenAIResponseGenerator(api_key="test_key")
        prompt = "Test prompt"
        response = generator.generate_response(prompt)

        self.assertEqual(response, "No response from OpenAI client")


if __name__ == "__main__":
    unittest.main()
