from gtts import gTTS
import re

def clean_text_for_audio(text):
    # remove quebras de linha
    text = text.replace("\n", " ")

    # remove emojis
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # remove símbolos tipo *, #, etc
    text = re.sub(r'[*#_`]', '', text)

    return text.strip()


def extract_english_part(text):
    """
    tenta pegar apenas frases em inglês
    estratégia simples: pega linhas que começam com letra maiúscula e não têm acentos
    """
    lines = text.split("\n")
    english_lines = []

    for line in lines:
        if re.match(r'^[A-Za-z ,.\'?!]+$', line.strip()):
            english_lines.append(line.strip())

    if not english_lines:
        return "Let's practice English!"

    return " ".join(english_lines)


def speak(text, filename="response.mp3"):
    english_text = extract_english_part(text)
    clean_text = clean_text_for_audio(english_text)

    tts = gTTS(text=clean_text, lang="en")
    tts.save(filename)

    return filename