from agents.conversation_agent import respond
from agents.grammar_agent import correct
from agents.interviewer_agent import interview
from memory.user_memory import get_user_profile, get_user_context


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
    profile = get_user_profile(user_id)

    # Saudação rápida
    if is_greeting(text):
        mensagem_texto = "Hello! How are you today?"
        mensagem_audio = "Hello! How are you today?"
        return {
            "text": mensagem_texto,
            "audio": mensagem_audio,
            "pt": None,
            "buttons": None
        }

    # Entrevistador
    interview_result = interview(text, user_id)

    if interview_result is not None and len(interview_result) == 4:
        entrevista_resposta, entrevista_audio, entrevista_pt, buttons = interview_result
        
        if entrevista_resposta is not None:
            return {
                "text": entrevista_resposta,
                "audio": entrevista_audio,
                "pt": entrevista_pt,
                "buttons": buttons
            }

    # 🤖 Conversation Agent
    user_context = get_user_context(user_id)
    en, pt = respond(text, user_id, user_context)

    # respostas naturais curtas não precisam de correção
    skip_correction = is_short_natural_reply(text)

    # 📝 Grammar Agent
    grammar_feedback = None
    if not skip_correction:
        grammar_feedback = correct(text)

    # resposta final
    mensagem_texto = f"{en}"

    # 💡 explicação opcional
    explicacao_pt = None
    if pt:
        explicacao_pt = pt

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

    # 🔊 áudio apenas em inglês
    mensagem_audio = en

    return {
        "text": mensagem_texto,
        "audio": mensagem_audio,
        "pt": explicacao_pt,
        "buttons": None
    }