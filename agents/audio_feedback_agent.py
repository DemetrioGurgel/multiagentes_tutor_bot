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

# Prompt para análise de áudio
audio_prompt = PromptTemplate(
    input_variables=["transcription"],
    template="""
Você é um especialista em pronúncia e interpretação de inglês falado.

Analise esta transcrição de áudio enviada por um aluno brasileiro aprendendo inglês:
"{transcription}"

Forneça feedback em português sobre:
1. Como o aluno falou (pronúncia aproximada baseada na transcrição)
2. Interpretação do que ele quis dizer
3. Dicas específicas para melhorar a pronúncia de palavras-chave

Seja encorajador e específico. Mantenha curto e direto.

FORMATO (sem os colchetes de exemplo):
Pronúncia: [análise curta]
Interpretação: [o que ele quis dizer]
Dicas: [sugestões práticas]
"""
)

def analyze_audio_feedback(transcription):
    if not transcription or len(transcription.strip()) < 3:
        return "Áudio muito curto para análise. Tente falar frases maiores!"

    final_prompt = audio_prompt.format(transcription=transcription)

    completion = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0.3
    )

    feedback = completion.choices[0].message.content.strip()

    return feedback