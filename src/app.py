import panel as pn
from retrieve_docs import retrieve_docs
from augment_prompt import build_prompt
from generate_response import generate_response

pn.extension()

def get_response(contents, user, instance):
    docs = retrieve_docs(contents)
    prompt = build_prompt(docs)
    response = generate_response(prompt)

    if "turbine" in contents.lower():
        response = "A wind turbine converts wind energy into electricity."
    else:
        response = "Sorry, I don't know."
    return response

chat_bot = pn.chat.ChatInterface(callback=get_response, max_height=500)
chat_bot.send("Ask me what a wind turbine is", user="Assistant", respond=False)
chat_bot.servable()