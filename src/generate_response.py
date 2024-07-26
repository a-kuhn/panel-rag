from abc import ABC, abstractmethod
from openai import OpenAI
from ollama import Client
import asyncio


class ResponseGenerator(ABC):
    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass


class OllamaResponseGenerator(ResponseGenerator):
    def __init__(self, host_url: str = "http://localhost:11434", model: str = "phi3"):
        super().__init__(model)
        self.client = Client(host=host_url)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Error generating Ollama response: {e}")
            return "No response from Ollama client"


class OpenAIResponseGenerator(ResponseGenerator):
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        super().__init__(model)
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating OpenAI response: {e}")
            return "No response from OpenAI client"
