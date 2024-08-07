import panel as pn
import os
from dotenv import load_dotenv
from retrieve import get_elasticsearch_client, retrieve_docs
from augment import build_prompt
from generate import get_ollama_client, get_openai_client

import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
pn.extension()


elasticsearch_host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
elasticsearch_client = get_elasticsearch_client(host_url="http://elasticsearch:9200")


ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama_client = get_ollama_client(host_url=ollama_host)

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = get_openai_client(api_key=openai_api_key)


def get_response(
    contents: str, user: str, instance: pn.chat.ChatInterface
) -> pn.chat.ChatMessage:
    docs, _ = retrieve_docs(contents, es_client=elasticsearch_client)
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
