from agents.conversation_agent import respond
from agents.grammar_agent import correct
from agents.pronunciation_agent import evaluate_pronunciation


def is_greeting(text):

    greetings = [
        "hello",
        "hi",
        "hey",
        "what's up",
        "ola",
        "olá"
    ]

    return text.lower().strip() in greetings


def is_short_natural_reply(text):

    natural_replies = [
        "me too",
        "me too!",
        "cool",
        "nice",
        "really?",
        "wow",
        "great",
        "awesome",
        "same",
        "yes",
        "no"
    ]

    return text.lower().strip() in natural_replies


def handle_message(text, user_id):

    # Saudação rápida
    if is_greeting(text):

        mensagem_texto = "Hello! How are you today?"
        mensagem_audio = "Hello! How are you today?"

        return mensagem_texto, mensagem_audio


    # 🤖 Conversation Agent
    en, pt = respond(text, user_id)


    # respostas naturais curtas não precisam de correção
    skip_correction = (
        is_short_natural_reply(text)
    )


    # 📝 Grammar Agent
    grammar_feedback = None

    if not skip_correction:

        grammar_feedback = correct(text)


    # 🎧 Pronunciation Agent
    pronunciation_feedback = evaluate_pronunciation(text)


    # resposta final
    mensagem_texto = f"{en}"


    # 💡 explicação opcional
    if pt:

        mensagem_texto += f"""

💡 {pt}
"""


    # 📝 correção opcional
    if (
        grammar_feedback
        and grammar_feedback not in [
            "Frase correta.",
            "Saudação simples correta.",
            "Frase compreensível."
        ]
    ):

        mensagem_texto += f"""

📝 {grammar_feedback}
"""


    # 🎧 pronúncia apenas em frases maiores
    if len(text.split()) >= 3:

        mensagem_texto += f"""

🎧 {pronunciation_feedback}
"""


    # 🔊 áudio apenas em inglês
    mensagem_audio = en


    return mensagem_texto, mensagem_audio