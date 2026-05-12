import os
from openai import OpenAI
from dotenv import load_dotenv
from memory.user_memory import (
    get_user_profile,
    has_used_word,
    record_used_word,
    has_used_structure,
    record_used_structure,
    has_used_sentence,
    record_used_sentence
)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

def normalize_text(text):
    return text.strip().lower()

def contains_item_text(user_text, item_text):
    user_text_norm = normalize_text(user_text)
    item_text_norm = normalize_text(item_text)
    return item_text_norm in user_text_norm

def get_item_text(item):
    return item["text"]

def generate_tutor_response(item_text, previous_user_sentence, previous_tutor_sentence=None):
    prompt = f"""
You are an English tutor helping a student practice vocabulary and sentence structures.
The student just said: "{previous_user_sentence}"
Previous tutor message: "{previous_tutor_sentence if previous_tutor_sentence else 'None'}"

Now you need to respond in English using the following word or structure naturally in your answer:
"{item_text}"

Your response should be a short, friendly sentence (1-2 sentences) that continues the conversation.
Make sure the required word/structure appears exactly as shown.
Do not add extra instructions. Just give your reply.
"""
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return completion.choices[0].message.content.strip()

def start_sequential_practice(user_id):
    profile = get_user_profile(user_id)
    items = profile.get("practice_items", [])
    if not items:
        return finish_practice_session(user_id)
    
    first_item = items[0]
    profile["practice_mode"] = "sequential_dialogue"
    profile["practice_user_last_item"] = None
    profile["practice_tutor_last_item"] = None
    profile["practice_next_tutor_index"] = 1
    profile["practice_dialogue_history"] = []
    profile["practice_last_user_sentence"] = ""
    profile["practice_last_tutor_sentence"] = ""
    
    instructions_en = f"Let's practice with a dialogue. First, write a sentence using: {get_item_text(first_item)}"
    instructions_pt = f"Vamos praticar com um diálogo. Primeiro, escreva uma frase usando: {get_item_text(first_item)}"
    return instructions_en, instructions_en, instructions_pt, None

def finish_practice_session(user_id):
    profile = get_user_profile(user_id)
    profile["mode"] = "conversation"
    for key in ["practice_mode", "practice_user_last_item", "practice_tutor_last_item", 
                "practice_next_tutor_index", "practice_dialogue_history", 
                "practice_last_user_sentence", "practice_last_tutor_sentence"]:
        if key in profile:
            del profile[key]
    return (
        "Excellent job! You finished the dialogue practice. Let's continue with normal English conversation.",
        "Excelente trabalho! Você terminou a prática de diálogo. Vamos continuar com a conversa normal em inglês.",
        None,
        None
    )

def handle_practice_step(text, user_id):
    profile = get_user_profile(user_id)
    if profile.get("mode") != "practice":
        return None, None, None, None

    items = profile.get("practice_items", [])
    if not items:
        return finish_practice_session(user_id)

    # Se não tiver practice_mode definido, inicia o modo sequencial
    if "practice_mode" not in profile or profile["practice_mode"] != "sequential_dialogue":
        return start_sequential_practice(user_id)

    # Verifica se já terminou (tutor já usou todos os itens)
    next_tutor_index = profile.get("practice_next_tutor_index", 0)
    if next_tutor_index >= len(items):
        return finish_practice_session(user_id)

    # Estado atual
    previous_user_sentence = profile.get("practice_last_user_sentence", "")
    previous_tutor_sentence = profile.get("practice_last_tutor_sentence", "")
    required_item = None

    # Se o tutor ainda não respondeu (começo), usuário deve usar o primeiro item
    if profile["practice_tutor_last_item"] is None:
        required_item = items[0]
    else:
        last_tutor_item_text = profile["practice_tutor_last_item"]
        for it in items:
            if it["text"] == last_tutor_item_text:
                required_item = it
                break
        if required_item is None:
            required_item = items[profile["practice_next_tutor_index"] - 1] if profile["practice_next_tutor_index"] > 0 else items[0]

    # Valida se o usuário usou o item obrigatório
    if not contains_item_text(text, required_item["text"]):
        return (
            f"Please try again and use the required word/structure: '{required_item['text']}'.",
            f"Por favor, tente novamente e use a palavra/estrutura: '{required_item['text']}'.",
            None,
            None
        )

    # Verifica se a frase já foi usada antes
    if has_used_sentence(user_id, text):
        return (
            "You've already used that sentence. Try a different one with the same word.",
            "Você já usou essa frase. Tente uma diferente com a mesma palavra.",
            None,
            None
        )

    # Registra a frase do usuário
    record_used_sentence(user_id, text)
    profile["practice_last_user_sentence"] = text

    # Tutor responde usando o próximo item
    tutor_index = profile["practice_next_tutor_index"]
    if tutor_index >= len(items):
        return finish_practice_session(user_id)

    tutor_item = items[tutor_index]
    tutor_item_text = get_item_text(tutor_item)

    tutor_response = generate_tutor_response(
        tutor_item_text,
        previous_user_sentence=text,
        previous_tutor_sentence=previous_tutor_sentence
    )

    if tutor_item["type"] == "words":
        record_used_word(user_id, tutor_item_text)
    else:
        record_used_structure(user_id, tutor_item_text)

    profile["practice_tutor_last_item"] = tutor_item_text
    profile["practice_last_tutor_sentence"] = tutor_response
    profile["practice_next_tutor_index"] = tutor_index + 1

    follow_up_msg = f"Great! Now try to use the same structure in your next sentence:\n\n{tutor_response}"
    follow_up_pt = f"Ótimo! Agora tente usar a mesma estrutura na sua próxima frase:\n\n{tutor_response}"

    return follow_up_msg, follow_up_msg, follow_up_pt, None