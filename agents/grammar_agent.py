import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def correct(text):
    prompt = f"""
    Corrija a frase em inglês e explique em português.

    Frase: "{text}"

    Resposta curta:
    - versão corrigida
    - explicação simples
    """

    response = model.generate_content(prompt)

    return response.text