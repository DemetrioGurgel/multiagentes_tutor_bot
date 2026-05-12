"""
Biblioteca IPA - Sons do Inglês para Falantes Portugueses
Sessão estática com sons organizados por categoria
"""

# Mapeamento de sons IPA para arquivos de áudio
IPA_AUDIO_MAPPING = {
    "/p/": {"word": "pig", "files": {"normal": "NORMAL-PIG.mp3", "phoneme": "PHONEME-PIG.mp3", "slow": "SLOW-PIG.mp3"}},
    "/b/": {"word": "bear", "files": {"normal": "NORMAL-BEAR.mp3", "phoneme": "PHONEME-BEAR.mp3", "slow": "SLOW-BEAR.mp3"}},
    "/t/": {"word": "turtle", "files": {"normal": "NORMAL-TURTLE.mp3", "phoneme": "PHONEME-TURTLE.mp3", "slow": "SLOW-TURTLE.mp3"}},
    "/d/": {"word": "dog", "files": {"normal": "NORMAL-DOG.mp3", "phoneme": "PHONEME-DOG.mp3", "slow": "SLOW-DOG.mp3"}},
    "/k/": {"word": "cat", "files": {"normal": "NORMAL-CAT.mp3", "phoneme": "PHONEME-CAT.mp3", "slow": "SLOW-CAT.mp3"}},
    "/g/": {"word": "goat", "files": {"normal": "NORMAL-GOAT.mp3", "phoneme": "PHONEME-GOAT.mp3", "slow": "SLOW-GOAT.mp3"}},
    
    "/θ/": {"word": "panther", "files": {"normal": "NORMAL-PANTHER.mp3", "phoneme": "PHONEME-PANTHER.mp3", "slow": "SLOW-PANTHER.mp3"}},
    "/ð/": {"word": "feather", "files": {"normal": "NORMAL-FEATHER.mp3", "phoneme": "PHONEME-FEATHER.mp3", "slow": "SLOW-FEATHER.mp3"}},
    "/f/": {"word": "frog", "files": {"normal": "NORMAL-FROG.mp3", "phoneme": "PHONEME-FROG.mp3", "slow": "SLOW-FROG.mp3"}},
    "/v/": {"word": "beaver", "files": {"normal": "NORMAL-BEAVER.mp3", "phoneme": "PHONEME-BEAVER.mp3", "slow": "SLOW-BEAVER.mp3"}},
    
    "/s/": {"word": "snake", "files": {"normal": "NORMAL-SNAKE.mp3", "phoneme": "PHONEME-SNAKE.mp3", "slow": "SLOW-SNAKE.mp3"}},
    "/z/": {"word": "zebra", "files": {"normal": "NORMAL-ZEBRA.mp3", "phoneme": "PHONEME-ZEBRA.mp3", "slow": "SLOW-ZEBRA.mp3"}},
    "/ʃ/": {"word": "sheep", "files": {"normal": "NORMAL-SHEEP.mp3", "phoneme": "PHONEME-SHEEP.mp3", "slow": "SLOW-SHEEP.mp3"}},
    "/ʒ/": {"word": "television", "files": {"normal": "NORMAL-TELEVISION.mp3", "phoneme": "PHONEME-TELEVISION.mp3", "slow": "SLOW-TELEVISION.mp3"}},
    "/tʃ/": {"word": "chicken", "files": {"normal": "NORMAL-CHICKEN.mp3", "phoneme": "PHONEME-CHICKEN.mp3", "slow": "SLOW-CHICKEN.mp3"}},
    "/dʒ/": {"word": "giraffe", "files": {"normal": "NORMAL-GIRAFFE.mp3", "phoneme": "PHONEME-GIRAFFE.mp3", "slow": "SLOW-GIRAFFE.mp3"}},
    
    "/w/": {"word": "wolf", "files": {"normal": "NORMAL-WOLF.mp3", "phoneme": "PHONEME-WOLF.mp3", "slow": "SLOW-WOLF.mp3"}},
    "/ɫ/": {"word": "lion", "files": {"normal": "NORMAL-LION.mp3", "phoneme": "PHONEME-LION.mp3", "slow": "SLOW-LION.mp3"}},
    
    "/m/": {"word": "mouse", "files": {"normal": "NORMAL-MOUSE.mp3", "phoneme": "PHONEME-MOUSE.mp3", "slow": "SLOW-MOUSE.mp3"}},
    "/n/": {"word": "dinosaur", "files": {"normal": "NORMAL-DINOSAUR.mp3", "phoneme": "PHONEME-DINOSAUR.mp3", "slow": "SLOW-DINOSAUR.mp3"}},
    "/ŋ/": {"word": "penguin", "files": {"normal": "NORMAL-PENGUIN.mp3", "phoneme": "PHONEME-PENGUIN.mp3", "slow": "SLOW-PENGUIN.mp3"}},
    
    "/ɹ/": {"word": "rabbit", "files": {"normal": "NORMAL-RABBIT.mp3", "phoneme": "PHONEME-RABBIT.mp3", "slow": "SLOW-RABBIT.mp3"}},
    "/j/": {"word": "yak", "files": {"normal": "NORMAL-YAK.mp3", "phoneme": "PHONEME-YAK.mp3", "slow": "SLOW-YAK.mp3"}},
    "/h/": {"word": "horse", "files": {"normal": "NORMAL-HORSE.mp3", "phoneme": "PHONEME-HORSE.mp3", "slow": "SLOW-HORSE.mp3"}},
    
    "/i/": {"word": "green", "files": {"normal": "NORMAL-GREEN.mp3", "phoneme": "PHONEME-GREEN.mp3", "slow": "SLOW-GREEN.mp3"}},
    "/u/": {"word": "blue", "files": {"normal": "NORMAL-BLUE.mp3", "phoneme": "PHONEME-BLUE.mp3", "slow": "SLOW-BLUE.mp3"}},
    "/ɪ/": {"word": "pink", "files": {"normal": "NORMAL-PINK.mp3", "phoneme": "PHONEME-PINK.mp3", "slow": "SLOW-PINK.mp3"}},
    "/u:/": {"word": "wood", "files": {"normal": "NORMAL-WOOD.mp3", "phoneme": "PHONEME-WOOD.mp3", "slow": "SLOW-WOOD.mp3"}},
    "/ə/": {"word": "dust", "files": {"normal": "NORMAL-DUST.mp3", "phoneme": "PHONEME-DUST.mp3", "slow": "SLOW-DUST.mp3"}},
    "/ɛ/": {"word": "red", "files": {"normal": "NORMAL-RED.mp3", "phoneme": "PHONEME-RED.mp3", "slow": "SLOW-RED.mp3"}},
    "/ɝ/": {"word": "purple", "files": {"normal": "NORMAL-PURPLE.mp3", "phoneme": "PHONEME-PURPLE.mp3", "slow": "SLOW-PURPLE.mp3"}},
    "/ɔ:/": {"word": "mauve", "files": {"normal": "NORMAL-MAUVE.mp3", "phoneme": "PHONEME-MAUVE.mp3", "slow": "SLOW-MAUVE.mp3"}},
    "/æ/": {"word": "sand", "files": {"normal": "NORMAL-SAND.mp3", "phoneme": "PHONEME-SAND.mp3", "slow": "SLOW-SAND.mp3"}},
    "/ɑ/": {"word": "coffee", "files": {"normal": "NORMAL-COFFEE.mp3", "phoneme": "PHONEME-COFFEE.mp3", "slow": "SLOW-COFFEE.mp3"}},
    
    "/eɪ/": {"word": "jade", "files": {"normal": "NORMAL-JADE.mp3", "phoneme": "PHONEME-JADE.mp3", "slow": "SLOW-JADE.mp3"}},
    "/aɪ/": {"word": "lime", "files": {"normal": "NORMAL-LIME.mp3", "phoneme": "PHONEME-LIME.mp3", "slow": "SLOW-LIME.mp3"}},
    "/aʊ/": {"word": "brown", "files": {"normal": "NORMAL-BROWN.mp3", "phoneme": "PHONEME-BROWN.mp3", "slow": "SLOW-BROWN.mp3"}},
    "/oʊ/": {"word": "gold", "files": {"normal": "NORMAL-GOLD.mp3", "phoneme": "PHONEME-GOLD.mp3", "slow": "SLOW-GOLD.mp3"}},
    "/ɔɪ/": {"word": "turquoise", "files": {"normal": "NORMAL-TURQUOISE.mp3", "phoneme": "PHONEME-TURQUOISE.mp3", "slow": "SLOW-TURQUOISE.mp3"}},
}

IPA_LIBRARY = {
    "vowels": {
        "title": "🔤 VOGAIS",
        "sounds": {
            "/iː/": {
                "portuguese": "🇧🇷 Parece: 'ii' longo",
                "mouth": "👄 Sorria levemente e estique o som",
                "examples": "🗣 see, green, eat",
                "tip": "💡 Som longo e tenso"
            },

            "/ɪ/": {
                "portuguese": "🇧🇷 Parece: 'i' curto e relaxado",
                "mouth": "👄 Boca semi-aberta, língua relaxada",
                "examples": "🗣 sit, fish, big",
                "tip": "💡 Mais curto que /iː/"
            },

            "/æ/": {
                "portuguese": "🇧🇷 Parece: entre 'é' e 'a'",
                "mouth": "👄 Abra bem a boca e abaixe a mandíbula",
                "examples": "🗣 cat, bad, hand",
                "tip": "💡 Um dos sons mais difíceis para brasileiros"
            },

            "/ʌ/": {
                "portuguese": "🇧🇷 Parece: 'â' neutro",
                "mouth": "👄 Boca relaxada e semi-aberta",
                "examples": "🗣 cup, luck, love",
                "tip": "💡 Som curto e central"
            }
        }
    },

    "consonants": {
        "title": "🔤 CONSOANTES DIFÍCEIS",
        "sounds": {
            "/θ/": {
                "portuguese": "🇧🇷 Não existe em português",
                "mouth": "👄 Coloque a língua entre os dentes e solte ar",
                "examples": "🗣 think, three, bath",
                "tip": "💡 Som sem vibração na garganta"
            },

            "/ð/": {
                "portuguese": "🇧🇷 Parecido com um 'd' suave",
                "mouth": "👄 Língua entre os dentes + vibração na garganta",
                "examples": "🗣 this, mother, they",
                "tip": "💡 Versão sonora do /θ/"
            },

            "/ɹ/": {
                "portuguese": "🇧🇷 'R' americano",
                "mouth": "👄 Enrole levemente a língua para trás sem tocar o céu da boca",
                "examples": "🗣 red, right, car",
                "tip": "💡 Não vibre a língua como no português"
            },

            "/ŋ/": {
                "portuguese": "🇧🇷 Som final de 'ing'",
                "mouth": "👄 Parte de trás da língua toca o céu da boca mole",
                "examples": "🗣 sing, long, running",
                "tip": "💡 O 'g' normalmente não é pronunciado"
            }
        }
    },

    "long_sounds": {
        "title": "🔤 SONS LONGOS",
        "sounds": {
            "/uː/": {
                "portuguese": "🇧🇷 Parece: 'uu' longo",
                "mouth": "👄 Lábios arredondados e projetados para frente",
                "examples": "🗣 food, blue, school",
                "tip": "💡 Som longo e fechado"
            },

            "/ɔː/": {
                "portuguese": "🇧🇷 Parece: 'ó' aberto e longo",
                "mouth": "👄 Boca aberta com lábios arredondados",
                "examples": "🗣 door, more, talk",
                "tip": "💡 Em muitos sotaques o 'r' pode mudar o som"
            }
        }
    }
}


def get_ipa_guide():
    """Retorna o guia completo de IPA formatado"""
    message = "🎯 <b>BIBLIOTECA IPA - SONS DO INGLÊS</b>\n\n"
    message += "📚 <i>Dicas especiais para falantes de português</i>\n\n"
    message += "💡 <b>Como usar:</b>\n"
    message += "• Pratique cada som lentamente\n"
    message += "• Compare com os sons em português\n"
    message += "• Use os exemplos para treinar\n"
    message += "• o símbolo '<b>ː</b>' significa um som mais longo \n\n"

    for category_key, category in IPA_LIBRARY.items():
        message += f"{category['title']}\n"
        message += "─" * 20 + "\n\n"

        for sound, details in category['sounds'].items():
            message += f"<b>{sound}</b>\n"
            message += f"{details['portuguese']}\n"
            message += f"{details['mouth']}\n"
            message += f"{details['examples']}\n"
            message += f"{details['tip']}\n\n"

    return message


def get_ipa_category(category_name):
    """Retorna uma categoria específica de sons"""
    if category_name not in IPA_LIBRARY:
        return "❌ Categoria não encontrada. Use: vowels, consonants, long_sounds"

    category = IPA_LIBRARY[category_name]
    message = f"{category['title']}\n"
    message += "─" * 20 + "\n\n"

    for sound, details in category['sounds'].items():
        message += f"<b>{sound}</b>\n"
        message += f"{details['portuguese']}\n"
        message += f"{details['mouth']}\n"
        message += f"{details['examples']}\n"
        message += f"{details['tip']}\n\n"

    return message


def get_ipa_sound(sound_symbol):
    """Retorna informações sobre um som específico"""
    return get_ipa_sound_with_audio(sound_symbol)


def get_ipa_sound_with_audio(sound_symbol):
    """Retorna informações sobre um som específico incluindo áudios disponíveis"""

    if sound_symbol in IPA_AUDIO_MAPPING:
        audio_info = IPA_AUDIO_MAPPING[sound_symbol]
        message = f"🎧 <b>{sound_symbol}</b>\n\n"
        message += f"📖 Palavra: <b>{audio_info['word']}</b>\n"
        message += f"▶️  Normal | 🔊 Fonema | 🐌 Lento\n\n"
        message += "💡 Use os botões abaixo para escutar."
        return message

    # 3. Nem descrição nem áudio → erro
    return f"❌ Som {sound_symbol} não encontrado na biblioteca."

def get_audio_buttons(sound_symbol):
    """Retorna lista de botões para tocar áudios de um som específico"""
    if sound_symbol not in IPA_AUDIO_MAPPING:
        return None
    
    audio_info = IPA_AUDIO_MAPPING[sound_symbol]
    buttons = []
    
    # Botão para áudio normal
    buttons.append({
        "id": f"audio_normal_{sound_symbol.replace('/', '')}",
        "text": f"▶️ {audio_info['word']} (normal)",
        "audio_file": f"mp3/{audio_info['files']['normal']}",
        "symbol": sound_symbol
    })
    
    # Botão para áudio do fonema
    buttons.append({
        "id": f"audio_phoneme_{sound_symbol.replace('/', '')}",
        "text": f"🔊 {audio_info['word']} (fonema)",
        "audio_file": f"mp3/{audio_info['files']['phoneme']}",
        "symbol": sound_symbol
    })
    
    # Botão para áudio lento
    buttons.append({
        "id": f"audio_slow_{sound_symbol.replace('/', '')}",
        "text": f"🐌 {audio_info['word']} (lento)",
        "audio_file": f"mp3/{audio_info['files']['slow']}",
        "symbol": sound_symbol
    })
    
    return buttons


def normalize_ipa_symbol(text):
    """Normaliza um símbolo IPA - adiciona barras se necessário e valida"""
    text = text.strip()
    
    # Se já tem barras, apenas retorna
    if text.startswith('/') and text.endswith('/'):
        return text
    
    # Senão, adiciona as barras
    symbol = f"/{text}/"
    
    # Verifica se existe no mapeamento
    if symbol in IPA_AUDIO_MAPPING:
        return symbol
    
    # Se não achou, tenta procurar por palavra
    for sym, info in IPA_AUDIO_MAPPING.items():
        if info['word'].lower() == text.lower():
            return sym
    
    return None


def get_ipa_help():
    """Retorna mensagem de ajuda para comandos IPA"""
    message = "🎯 <b>COMO USAR A BIBLIOTECA IPA</b>\n\n"
    
    message += "<b>📚 VER CATEGORIAS:</b>\n"
    message += "/ipa - Guia completo com todos os sons\n\n"
    
    message += "<b>🎧 OUVIR ÁUDIOS:</b>\n\n"
    message += "/ipa /p/ - Mostra som /p/ em três exemplos\n"
    message += "/ipa /θ/ - Mostra som /θ/ em três exemplos\n"
    message += "/ipa /i/ - Mostra som /i/ em três exemplos\n\n"
    
    return message