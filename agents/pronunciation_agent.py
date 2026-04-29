def evaluate_pronunciation(user_text):
    feedback = "Sua pronúncia está compreensível, mas tente articular melhor as palavras."

    if len(user_text.split()) < 3:
        feedback = "Tente falar frases completas para melhorar sua prática de pronúncia."

    return feedback

