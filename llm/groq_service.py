
import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqService:

    def __init__(self):
        api_key = None

        try:
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró GROQ_API_KEY en Streamlit Secrets ni en .env."
            )

        api_key = api_key.strip()

        fingerprint = hashlib.sha256(
            api_key.encode()
        ).hexdigest()[:12]

        print(
            f"[GROQ DIAGNOSTIC] "
            f"Longitud: {len(api_key)} | "
            f"Prefijo correcto: {api_key.startswith('gsk_')} | "
            f"Huella: {fingerprint}"
        )

        self.client = Groq(api_key=api_key)

    def ask(self, prompt: str, system_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
