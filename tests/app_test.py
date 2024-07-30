import pytest
from unittest.mock import patch, MagicMock
import os
from src.app import (
    get_openai_client,
    get_ollama_client,
    get_response,
)


@patch.dict(os.environ, {"OPENAI_API_KEY": "test_api_key"})
def test_get_openai_client():
    from src.app import (
        OpenAIResponseGenerator,
    )

    client = get_openai_client(api_key="test_api_key", model="gpt-4o")
    assert isinstance(client, OpenAIResponseGenerator)
    assert client.api_key == "test_api_key"
    assert client.model == "gpt-4o"


def test_get_openai_client_no_api_key():
    with patch.dict(os.environ, {}, clear=True):
        print(os.environ)
        print(os.getenv("OPENAI_API_KEY"))
        with pytest.raises(
            ValueError, match="OPENAI_API_KEY not found in environment variables"
        ):
            get_openai_client()


def test_get_ollama_client():
    from src.app import (
        OllamaResponseGenerator,
    )

    client = get_ollama_client()
    assert isinstance(client, OllamaResponseGenerator)
    assert client.host_url == "http://localhost:11434"
    assert client.model == "phi3"


@patch("src.app.retrieve_docs")
@patch("src.app.build_prompt")
@patch("src.app.OpenAIResponseGenerator.generate_response")
def test_get_response(mock_generate_response, mock_build_prompt, mock_retrieve_docs):
    mock_retrieve_docs.return_value = (["doc1", "doc2"], None)
    mock_build_prompt.return_value = "test prompt"
    mock_generate_response.return_value = "test response"

    contents = "Test contents"
    user = "Test user"
    instance = MagicMock()
    response = get_response(contents, user, instance)

    mock_retrieve_docs.assert_called_once_with(contents)
    mock_build_prompt.assert_called_once_with(
        question=contents, context_docs=["doc1", "doc2"]
    )
    mock_generate_response.assert_called_once_with("test prompt")

    assert response.object == "test response"
    assert response.user == "Zoomcamp TA"
    assert response.avatar == "🚀"
