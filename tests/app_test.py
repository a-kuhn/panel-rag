import pytest
from unittest.mock import patch, MagicMock
import panel as pn
from src.app import get_response


@pytest.fixture
def mock_retrieve_docs():
    with patch("src.app.retrieve_docs") as mock:
        yield mock


@pytest.fixture
def mock_build_prompt():
    with patch("src.app.build_prompt") as mock:
        yield mock


@pytest.fixture
def mock_generate_response():
    with patch("src.app.ollama_client.generate_response") as mock:
        yield mock


@pytest.fixture
def chat_interface_instance():
    return MagicMock(spec=pn.chat.ChatInterface)


def test_get_response(
    mock_retrieve_docs,
    mock_build_prompt,
    mock_generate_response,
    chat_interface_instance,
):
    # Arrange
    mock_retrieve_docs.return_value = (["doc1", "doc2"], None)
    mock_build_prompt.return_value = "mock_prompt"
    mock_generate_response.return_value = "mock_response"

    contents = "What is the Zoomcamp?"
    user = "confused student"

    # Act
    response = get_response(contents, user, chat_interface_instance)

    # Assert
    assert isinstance(response, pn.chat.ChatMessage)
    assert response.object == "mock_response"
    assert response.user == "Zoomcamp TA"
    assert response.avatar == "🚀"
