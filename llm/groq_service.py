
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqService:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "Falta configurar GROQ_API_KEY en el archivo .env."
            )

        self.client = Groq(api_key=api_key)

    def ask(self, prompt: str, system_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

