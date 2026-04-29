from agents.conversation_agent import respond
from agents.pronunciation_agent import evaluate_pronunciation


def is_greeting(text):
    greetings = ["hello", "hi", "hey", "what's up", "ola", "olá"]
    return text.lower().strip() in greetings


def handle_message(text):
    # Saudação → resposta direta (rápida)
    if is_greeting(text):
        mensagem_texto = "Hello! How are you today? "
        mensagem_audio = "Hello! How are you today?"
        return mensagem_texto, mensagem_audio

    # IA (agora retorna EN + PT separados)
    en, pt = respond(text)

    # pronúncia (PT)
    pronuncia = evaluate_pronunciation(text)

    # mensagem completa (Telegram)
    mensagem_texto = f"{en}\n\n {pt}\n {pronuncia}"

    # áudio (SOMENTE inglês)
    mensagem_audio = en

    return mensagem_texto, mensagem_audio