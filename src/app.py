import panel as pn
import os
from dotenv import load_dotenv
from retrieve_docs import retrieve_docs
from augment_prompt import build_prompt
from generate_response import OpenAIResponseGenerator, OllamaResponseGenerator

load_dotenv()
pn.extension()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAIResponseGenerator(api_key=openai_api_key)

ollama_client = OllamaResponseGenerator()


def get_response(contents, user, instance):
    docs, _ = retrieve_docs(contents)
    prompt = build_prompt(question=contents, context_docs=docs)
    response = ollama_client.generate_response(prompt)
    return pn.chat.ChatMessage(response, user="Zoomcamp TA", avatar="🚀")


chat_interface = pn.chat.ChatInterface(
    callback=get_response,
    callback_user="Zoomcamp TA",
    max_height=500,
    user="confused student",
    # user_avatar="🤓",
    show_undo=False,
)
chat_interface.send(
    "Ask me about the Zoomcamp courses", respond=False, user="Zoomcamp TA", avatar="🚀"
)
chat_interface.servable()
