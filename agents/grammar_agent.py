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
- Máximo 2 frases por seção
- Não explique demais
- Não seja robótico
- Não repita a frase original desnecessariamente
- Não corrija frases que já sejam naturais

COMPORTAMENTO:
- Se for apenas uma saudação simples, responda:
"Saudação simples correta."

- Se a frase estiver correta, responda:
"Frase correta."

- Se houver erro gramatical importante:
mostre a correção natural em inglês E dê uma dica prática sobre construção frasal

- Expressões curtas naturais como "Me too", "Nice", "Cool", "Really?" devem ser consideradas corretas

FORMATO:
CORRECTION: [texto de correção ou "Frase correta."]
TIP: [dica de construção frasal se houver erro, senão deixe em branco]

EXEMPLOS:

Entrada:
hello

Saída:
CORRECTION: Saudação simples correta.
TIP: 

Entrada:
i did a travel

Saída:
CORRECTION: I took a trip.
TIP: Use "take a trip" em vez de "do a travel" - "take" é mais natural para viagens.

Entrada:
I'd like to speak about cars

Saída:
CORRECTION: Frase correta.
TIP: 

Entrada:
She go to school

Saída:
CORRECTION: She goes to school.
TIP: Com third person (she, he, it), adicione -s ao verbo no presente simples.
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
    tip = ""


    # extrai resposta
    for line in content.split("\n"):

        if line.startswith("CORRECTION:"):

            correction = line.replace(
                "CORRECTION:",
                ""
            ).strip()

        elif line.startswith("TIP:"):

            tip = line.replace(
                "TIP:",
                ""
            ).strip()


    # fallback
    if not correction:
        correction = "Frase compreensível."

    # Combinar correção e dica
    if tip:
        return f"{correction} {tip}"
    else:
        return correction