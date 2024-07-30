import pytest
from unittest.mock import MagicMock, patch
from src.generate_response import OllamaResponseGenerator, OpenAIResponseGenerator


@patch("src.generate_response.Client")
def test_ollama_response_generator(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = {"message": {"content": "mocked response"}}
    mock_client.chat.return_value = mock_response

    generator = OllamaResponseGenerator()
    response = generator.generate_response("test prompt")

    assert response == "mocked response"
    mock_client.chat.assert_called_once_with(
        model="phi3", messages=[{"role": "user", "content": "test prompt"}]
    )


@patch("src.generate_response.Client")
def test_ollama_response_generator_exception(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_client.chat.side_effect = Exception("Test Exception")

    generator = OllamaResponseGenerator()
    response = generator.generate_response("test prompt")

    assert response == "No response from Ollama client"


@patch("src.generate_response.OpenAI")
def test_openai_response_generator(mock_openai_class):
    mock_openai_client = MagicMock()
    mock_openai_class.return_value = mock_openai_client

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="mocked response"))]
    mock_openai_client.chat.completions.create.return_value = mock_response

    generator = OpenAIResponseGenerator(api_key="test_key")
    response = generator.generate_response("test prompt")

    assert response == "mocked response"
    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4o", messages=[{"role": "user", "content": "test prompt"}]
    )


@patch("src.generate_response.OpenAI")
def test_openai_response_generator_exception(mock_openai_class):
    mock_openai_client = MagicMock()
    mock_openai_class.return_value = mock_openai_client

    mock_openai_client.chat.completions.create.side_effect = Exception("Test Exception")

    generator = OpenAIResponseGenerator(api_key="test_key")
    response = generator.generate_response("test prompt")

    assert response == "No response from OpenAI client"


if __name__ == "__main__":
    pytest.main()
