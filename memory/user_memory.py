from langchain_community.chat_message_histories import ChatMessageHistory

# memória por usuário
user_memories = {}
user_profiles = {}

def get_memory(user_id):

    if user_id not in user_memories:

        user_memories[user_id] = ChatMessageHistory()

    return user_memories[user_id]


def get_user_profile(user_id):

    if user_id not in user_profiles:

        user_profiles[user_id] = {
            "mode": "conversation",
            "interview_stage": 0,
            "interview_responses": [],
            "pending_response": None,
            "goal": None,
            "roadmap": None,
            "practice_topic": None,
            "practice_subtopic": None,
            "practice_items": [],
            "practice_index": 0,
            "practice_stage": "ask_sentence",
            "practice_sentence": None,
            "used_words": [],
            "used_structures": [],
            "used_sentences": []
        }

    return user_profiles[user_id]


def reset_interview(user_id):

    profile = get_user_profile(user_id)
    profile["mode"] = "conversation"
    profile["interview_stage"] = 0
    profile["interview_responses"] = []
    profile["pending_response"] = None
    profile["goal"] = None
    profile["roadmap"] = None
    profile["practice_topic"] = None
    profile["practice_subtopic"] = None
    profile["practice_items"] = []
    profile["practice_index"] = 0
    profile["practice_stage"] = "ask_sentence"
    profile["practice_sentence"] = None
    profile["used_words"] = []
    profile["used_structures"] = []
    profile["used_sentences"] = []
    return profile


def has_used_word(user_id, word):
    profile = get_user_profile(user_id)
    return word.lower() in [w.lower() for w in profile.get("used_words", [])]


def record_used_word(user_id, word):
    profile = get_user_profile(user_id)
    if not has_used_word(user_id, word):
        profile.setdefault("used_words", []).append(word)


def has_used_structure(user_id, structure):
    profile = get_user_profile(user_id)
    return structure.lower() in [s.lower() for s in profile.get("used_structures", [])]


def record_used_structure(user_id, structure):
    profile = get_user_profile(user_id)
    if not has_used_structure(user_id, structure):
        profile.setdefault("used_structures", []).append(structure)


def has_used_sentence(user_id, sentence):
    profile = get_user_profile(user_id)
    normalized = sentence.strip().lower()
    return normalized in [s.strip().lower() for s in profile.get("used_sentences", [])]


def record_used_sentence(user_id, sentence):
    profile = get_user_profile(user_id)
    if not has_used_sentence(user_id, sentence):
        profile.setdefault("used_sentences", []).append(sentence)


def get_user_context(user_id):

    profile = get_user_profile(user_id)

    if not profile.get("goal") or not profile.get("roadmap"):
        return ""

    # Resumir em 1-2 frases
    goal = profile["goal"]
    roadmap_lines = profile["roadmap"].split("\n")
    level = ""
    for line in roadmap_lines:
        if line.startswith("Level:"):
            level = line.replace("Level:", "").strip()
            break

    context = f"The user is an {level} English learner with the goal: {goal}. They are following a personalized roadmap to improve."

    return context
