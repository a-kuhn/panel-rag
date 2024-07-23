from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def generate_openai_response(prompt: str, model: str = "gpt-4o") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content
    return answer
