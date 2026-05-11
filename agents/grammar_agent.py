from openai import OpenAI

from langchain_core.prompts import PromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()


# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# Prompt
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
Você é um corretor gramatical de inglês para brasileiros.

Analise a frase:
"{user_input}"

REGRAS:
- Seja extremamente curto
- Máximo 1 frase
- Não use markdown
- Não use emojis
- Não explique demais
- Não seja robótico
- Não repita a frase original desnecessariamente
- Não corrija frases que já sejam compreensíveis e naturais

COMPORTAMENTO:
- Se for apenas uma saudação simples, responda:
"Saudação simples correta."

- Se a frase estiver correta, responda:
"Frase correta."

- Se houver erro gramatical importante:
mostre apenas a correção natural em inglês

- Expressões curtas naturais como "Me too", "Nice", "Cool", "Really?" devem ser consideradas corretas

FORMATO:
CORRECTION: texto

EXEMPLOS:

Entrada:
hello

Saída:
CORRECTION: Saudação simples correta.

Entrada:
i did a travel

Saída:
CORRECTION: I took a trip.

Entrada:
I'd like to speak about cars

Saída:
CORRECTION: Frase correta.
"""
)


# Função principal
def correct(text):

    final_prompt = prompt.format(
        user_input=text
    )


    completion = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ]
    )


    content = completion.choices[0].message.content


    correction = ""


    # extrai resposta
    for line in content.split("\n"):

        if line.startswith("CORRECTION:"):

            correction = line.replace(
                "CORRECTION:",
                ""
            ).strip()


    # fallback
    if not correction:
        correction = "Frase compreensível."


    return correction