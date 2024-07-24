import panel as pn
from retrieve_docs import retrieve_docs
from augment_prompt import build_prompt
from generate_response import generate_openai_response

pn.extension()


def get_response(contents, user, instance):
    docs, _ = retrieve_docs(contents)
    prompt = build_prompt(question=contents, context_docs=docs)
    response = generate_openai_response(prompt)
    print("\n********************************")
    print(f"found docs from elasticsearch: {docs}\n\nand their scores: {_}")
    print("\n********************************")
    print(f"submitting prompt to openai: {prompt}")
    print("\n********************************")
    print(f"openai response: {response}")
    return response


chat_bot = pn.chat.ChatInterface(
    callback=get_response,
    callback_user="Zoomcamp TA",
    callback_avatar="🚀",
    max_height=500,
    user="confused student",
    user_avatar="🤓",
    show_undo=False,
)
chat_bot.send(
    "Ask me about the Zoomcamp courses", respond=False, user="Zoomcamp TA", avatar="🚀"
)
chat_bot.servable()
