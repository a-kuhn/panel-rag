import panel as pn
import os
from dotenv import load_dotenv
from retrieve_docs import retrieve_docs
from augment_prompt import build_prompt
from generate_response import OpenAIResponseGenerator, OllamaResponseGenerator

load_dotenv()
pn.extension()

openai_api_key = os.getenv("OPENAI_API_KEY")


def get_openai_client(
    api_key: str = None, model: str = "gpt-4o"
) -> OpenAIResponseGenerator:
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAIResponseGenerator(api_key=api_key, model=model)


def get_ollama_client(
    host_url: str = "http://localhost:11434", model: str = "phi3"
) -> OllamaResponseGenerator:
    return OllamaResponseGenerator(host_url=host_url, model=model)


openai_client = get_openai_client(api_key=openai_api_key)
ollama_client = get_ollama_client()


def get_response(
    contents: str, user: str, instance: pn.chat.ChatInterface
) -> pn.chat.ChatMessage:
    docs, _ = retrieve_docs(contents)
    prompt = build_prompt(question=contents, context_docs=docs)
    response = ollama_client.generate_response(prompt)
    return pn.chat.ChatMessage(object=response, user="Zoomcamp TA", avatar="🚀")


chat_interface = pn.chat.ChatInterface(
    callback=get_response,
    callback_user="Zoomcamp TA",
    max_height=500,
    user="confused student",
    show_undo=False,
)
chat_interface.send(
    "Ask me about the Zoomcamp courses", respond=False, user="Zoomcamp TA", avatar="🚀"
)
chat_interface.servable()
