
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqService:

    def __init__(self):
        api_key = None

        # Primero intenta obtener la clave de Streamlit Cloud
        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

        # Si no existe, utiliza el archivo .env local
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró GROQ_API_KEY en Streamlit Secrets ni en .env."
            )

        self.client = Groq(api_key=api_key.strip())

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
