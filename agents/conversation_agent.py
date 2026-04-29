import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def respond(text):
    prompt = f"""
Você é um tutor de inglês para brasileiros iniciantes.

OBJETIVO:
Ajudar o aluno a melhorar o inglês de forma simples, rápida e natural.

ENTRADA DO ALUNO:
"{text}"

REGRAS IMPORTANTES:
- Responda de forma MUITO curta (máximo 2 frases no total)
- NÃO use markdown, símbolos (*, #, -, etc.)
- NÃO use emojis
- NÃO escreva textos longos
- Seja direto e natural

COMPORTAMENTO:
- Se for uma frase correta → apenas elogie rapidamente
- Se tiver erro → corrija de forma simples
- Se for algo muito curto (ex: "hello") → apenas responda naturalmente

FORMATO OBRIGATÓRIO:
EN: frase em inglês (resposta principal)
PT: explicação curta em português (se necessário)

EXEMPLOS:

Entrada: "hello"
Saída:
EN: Hello! How are you?
PT: Saudação comum em inglês

Entrada: "i did a travel"
Saída:
EN: I took a trip.
PT: Usamos "take a trip" em vez de "do a travel"

Agora responda:
"""

    response = model.generate_content(prompt).text

    en = ""
    pt = ""

    for line in response.split("\n"):
        if line.startswith("EN:"):
            en = line.replace("EN:", "").strip()
        elif line.startswith("PT:"):
            pt = line.replace("PT:", "").strip()

    return en, pt