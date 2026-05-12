import logging
import time
import os

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from telegram.constants import ParseMode

from agents.orchestrator import handle_message
from audio.tts import speak
from ipa_library import get_ipa_guide, get_ipa_category, get_ipa_sound, get_ipa_help, get_audio_buttons, normalize_ipa_symbol


# Carrega variáveis .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configuração de logs
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_MAX_MESSAGE_CHARS = 3900


def truncate_text(text, limit=TELEGRAM_MAX_MESSAGE_CHARS):
    if not text:
        return ""

    if len(text) <= limit:
        return text

    truncated = text[:limit]
    if "\n" in truncated:
        truncated = truncated[:truncated.rfind("\n")]
    return f"{truncated.rstrip()}\n\n...message truncated for Telegram."


def truncate_section(section_text, limit):
    if not section_text:
        return ""

    if len(section_text) <= limit:
        return section_text

    truncated = section_text[:limit]
    if "\n" in truncated:
        truncated = truncated[:truncated.rfind("\n")]
    return f"{truncated.rstrip()}\n... (texto cortado)"


def build_audio_reply_text(mensagem_texto, texto, audio_feedback, grammar_feedback):
    mensagem_texto = truncate_section(mensagem_texto, 2200)
    full_message = mensagem_texto

    full_message += f"\n\n{'─' * 20}"
    full_message += "\n👨‍🏫 Speech Coach"
    full_message += f"\n{'─' * 20}"
    full_message += f"\n🎤 You said: {texto}"

    if audio_feedback:
        full_message += f"\n\n{'─' * 20}"
        full_message += "\n📊 Feedback"
        full_message += f"\n{'─' * 20}"
        full_message += f"\n{truncate_section(audio_feedback, 1200)}"

    if grammar_feedback and grammar_feedback not in [
        "Frase correta.",
        "Saudação simples correta.",
        "Frase compreensível."
    ]:
        full_message += f"\n\n{'─' * 20}"
        full_message += "\n📝 Grammar Tips"
        full_message += f"\n{'─' * 20}"
        full_message += f"\n{truncate_section(grammar_feedback, 800)}"

    return truncate_text(full_message)


# IPA COMMAND
async def handle_ipa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args if context.args else []

    logger.info(f"[IPA] Usuário: {user.id} | Args: {args}")

    try:
        if not args:
            # Comando /ipa sem argumentos - mostra guia completo
            message = get_ipa_guide()
        elif len(args) == 1:
            arg = args[0].lower()
            if arg in ['vowels', 'consonants', 'long_sounds']:
                # Comando /ipa categoria
                message = get_ipa_category(arg)
            else:
                # Tenta normalizar como símbolo IPA
                normalized_symbol = normalize_ipa_symbol(arg)
                
                if normalized_symbol:
                    # Símbolo IPA válido - mostra com botões de áudio
                    message = get_ipa_sound(normalized_symbol)
                    
                    # Verificar se há botões de áudio disponíveis
                    audio_buttons = get_audio_buttons(normalized_symbol)
                    keyboard = None
                    if audio_buttons:
                        keyboard = []
                        for button in audio_buttons:
                            keyboard.append([
                                InlineKeyboardButton(
                                    button["text"], 
                                    callback_data=button["id"]
                                )
                            ])
                        keyboard = InlineKeyboardMarkup(keyboard)
                    
                    await update.message.reply_text(
                        message,
                        reply_markup=keyboard,
                        parse_mode=ParseMode.HTML
                    )
                    return
                else:
                    # Símbolo não encontrado - mostra ajuda
                    message = get_ipa_help()
        else:
            # Múltiplos argumentos - mostra ajuda
            message = get_ipa_help()

        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        logger.error(f"[ERROR] Falha no handle_ipa: {e}")
        await update.message.reply_text(
            "❌ Erro ao carregar biblioteca IPA. Tente novamente."
        )


# START
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    logger.info(
        f"[START] Usuário: {user.id} iniciou o bot"
    )

    # Mensagem com os truques do English Tutor
    await update.message.reply_text(
        "<b>🎓 Bem-vindo ao English Tutor!</b>\n\n"
        "<b>📚 COMANDOS E HABILIDADES:</b>\n\n"
        
        "<b>🎤 Modo Entrevista:</b>\n"
        "• <i>interview</i> - Avalia seu interesse com algumas perguntas\n\n"
        
        "<b>💬 Modo Conversação:</b>\n"
        "• Escreva ou fale em inglês normalmente\n"
        "• Receba respostas personalizadas do seu tutor\n"
        "• Feedback de gramática e pronúncia em tempo real\n\n"
        
        "<b>🎵 Biblioteca IPA para brasileiros:</b>\n\n"

        "<b>📖 VER CATEGORIAS:</b>\n"
        "• <i>/ipa</i> - Guia escrito com tutorial e sons equivalentes\n\n"
        
        "<b>🎧 OUVIR ÁUDIOS IPA (escolha uma forma):</b>\n"
        "  /ipa /p/ → Mostra /p/ em 3 exemplos\n"
        "  /ipa /θ/ → Mostra /θ/ em 3 exemplos\n"
        "  /ipa /i/ → Mostra /i/ em 3 exemplos\n\n"

        "<b>📝 Recursos Extras:</b>\n"
        "• Envie áudios em inglês para praticar e receber feedback\n"
        "• Dicas de gramática personalizadas\n"
        "• Explicações em português quando necessário\n\n"
        
        "Vamos começar? Escolha uma opção acima! 🚀",
        parse_mode=ParseMode.HTML
    )


# CALLBACK (atualizado para usar o last_pt mais recente)
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    logger.info(f"[CALLBACK] Usuário: {query.from_user.id} | Data: {query.data}")

    # Se for callback de tradução
    if query.data.startswith("show_translation"):
        pt_text = context.user_data.get("last_pt")
        if pt_text:
            # Adiciona a tradução ao final da mensagem atual
            await query.edit_message_text(
                text=query.message.text + f"\n\n💡 {pt_text}",
                parse_mode=ParseMode.HTML
            )
        else:
            await query.edit_message_text(
                text=query.message.text + "\n\n❌ No translation available at this moment."
            )
    
    # Se for callback da entrevista (confirm/retry)
    elif query.data in ["confirm", "retry"]:
        await handle_interview_callback(update, context)


# TEXTO
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()

    user = update.effective_user
    user_text = update.message.text

    logger.info(
        f"[TEXT] Usuário: {user.id} | Mensagem: {user_text}"
    )

    try:
        logger.info("[FLOW] Enviando para orquestrador...")

        result = handle_message(user_text, user.id)

        # Extrair dados do resultado
        mensagem_texto = result["text"]
        mensagem_audio = result["audio"]
        explicacao_pt = result.get("pt")
        buttons = result.get("buttons")

        # ✅ Atualiza a tradução mais recente para o botão "Show translation"
        if explicacao_pt:
            context.user_data["last_pt"] = explicacao_pt

        logger.info("[FLOW] Gerando áudio (TTS)...")
        audio_file = speak(mensagem_audio)

        logger.info("[FLOW] Enviando resposta ao usuário...")

        # Criar markup dos botões
        reply_markup = None
        
        # Se tiver botões da entrevista, usar eles
        if buttons:
            keyboard = []
            for button in buttons:
                keyboard.append([
                    InlineKeyboardButton(
                        button["text"], 
                        callback_data=button["id"]
                    )
                ])
            reply_markup = InlineKeyboardMarkup(keyboard)
        # Se não tiver botões da entrevista mas tiver tradução, mostrar botão de tradução
        elif explicacao_pt:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("💡 Show translation", callback_data="show_translation")]
            ])

        await update.message.reply_text(
            truncate_text(mensagem_texto),
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

        await update.message.reply_voice(
            voice=open(audio_file, "rb")
        )

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"[SUCCESS] Resposta enviada em {elapsed}s")

    except Exception as e:
        logger.error(f"[ERROR] Falha no handle_text: {e}")


# ÁUDIO
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    user = update.effective_user

    logger.info(f"[AUDIO] Usuário: {user.id} enviou áudio")

    try:
        logger.info("[FLOW] Baixando áudio...")
        file = await update.message.voice.get_file()
        file_path = "audio.ogg"
        await file.download_to_drive(file_path)

        logger.info("[FLOW] Transcrevendo áudio (STT)...")
        from audio.stt import transcribe
        texto = transcribe(file_path)
        logger.info(f"[STT] Texto transcrito: {texto}")

        logger.info("[FLOW] Enviando para orquestrador...")
        result = handle_message(texto, user.id)

        # Extrair dados do resultado
        mensagem_texto = result["text"]
        mensagem_audio = result["audio"]
        explicacao_pt = result.get("pt")
        buttons = result.get("buttons")

        # ✅ Atualiza a tradução mais recente para o botão "Show translation"
        if explicacao_pt:
            context.user_data["last_pt"] = explicacao_pt

        logger.info("[FLOW] Analisando feedback de áudio...")
        from agents.audio_feedback_agent import analyze_audio_feedback
        audio_feedback = analyze_audio_feedback(texto)

        logger.info("[FLOW] Analisando feedback gramatical...")
        from agents.grammar_agent import correct
        grammar_feedback = correct(texto)

        logger.info("[FLOW] Gerando áudio (TTS)...")
        audio_file = speak(mensagem_audio)

        logger.info("[FLOW] Enviando resposta ao usuário...")

        # Criar markup dos botões
        reply_markup = None
        
        if buttons:
            keyboard = []
            for button in buttons:
                keyboard.append([
                    InlineKeyboardButton(
                        button["text"], 
                        callback_data=button["id"]
                    )
                ])
            reply_markup = InlineKeyboardMarkup(keyboard)
        elif explicacao_pt:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("💡 Show translation", callback_data="show_translation")]
            ])

        # Estruturar mensagem com ordem: resposta -> coach de fala -> feedback
        full_message = build_audio_reply_text(
            mensagem_texto,
            texto,
            audio_feedback,
            grammar_feedback
        )

        await update.message.reply_text(
            full_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )

        await update.message.reply_voice(
            voice=open(audio_file, "rb")
        )

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"[SUCCESS] Áudio processado em {elapsed}s")

    except Exception as e:
        logger.error(f"[ERROR] Falha no handle_audio: {e}")


# CALLBACK PARA BOTÕES DA ENTREVISTA
async def handle_interview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    action = query.data  # 'confirm' ou 'retry'
    
    logger.info(f"[INTERVIEW CALLBACK] Usuário: {user_id} | Ação: {action}")
    
    try:
        from agents.interviewer_agent import handle_interview_action
        
        result = handle_interview_action(action, user_id)
        
        if result and len(result) == 4:
            text, audio, pt, buttons = result
            
            # ✅ Atualiza a tradução mais recente para esta pergunta
            if pt:
                context.user_data["last_pt"] = pt
            
            if text:
                # Criar novos botões se necessário
                reply_markup = None
                if buttons:
                    keyboard = []
                    for button in buttons:
                        keyboard.append([
                            InlineKeyboardButton(
                                button["text"], 
                                callback_data=button["id"]
                            )
                        ])
                    reply_markup = InlineKeyboardMarkup(keyboard)
                # Se não houver botões da entrevista mas houver tradução, oferecer botão de tradução
                elif pt:
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("💡 Show translation", callback_data="show_translation")]
                    ])
                
                # Editar a mensagem existente (mostra o texto em inglês)
                await query.edit_message_text(
                    text=truncate_text(text),
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
                
                # Gerar e enviar áudio
                if audio:
                    logger.info("[INTERVIEW CALLBACK] Gerando áudio (TTS)...")
                    audio_file = speak(audio)
                    
                    await context.bot.send_voice(
                        chat_id=query.message.chat_id,
                        voice=open(audio_file, "rb")
                    )
                
                logger.info("[INTERVIEW CALLBACK] Resposta processada com sucesso")
    
    except Exception as e:
        logger.error(f"[ERROR] Falha no handle_interview_callback: {e}")


async def handle_ipa_audio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callbacks for IPA audio buttons"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data.startswith("audio_"):
        parts = callback_data.split("_")
        if len(parts) != 3:
            await query.answer("❌ Callback inválido", show_alert=True)
            return

        audio_type = parts[1]  # normal, phoneme, slow
        symbol_key = parts[2]
        sound_symbol = f"/{symbol_key}/"
        
        audio_buttons = get_audio_buttons(sound_symbol)
        if not audio_buttons:
            await query.answer("❌ Som IPA não encontrado para este botão", show_alert=True)
            return

        for button in audio_buttons:
            if button["id"] == callback_data:
                audio_file = button["audio_file"]
                
                try:
                    with open(audio_file, 'rb') as audio:
                        await context.bot.send_audio(
                            chat_id=query.message.chat_id,
                            audio=audio,
                            title=f"IPA Audio - {sound_symbol}",
                            caption=f"🎵 Áudio {audio_type} para o som {sound_symbol}",
                            parse_mode='HTML'
                        )
                        logger.info(f"[IPA AUDIO] Enviado arquivo: {audio_file}")
                except FileNotFoundError:
                    await query.answer(f"❌ Arquivo de áudio não encontrado: {audio_file}", show_alert=True)
                    logger.error(f"[IPA AUDIO] Arquivo não encontrado: {audio_file}")
                except Exception as e:
                    await query.answer(f"❌ Erro ao enviar áudio: {str(e)}", show_alert=True)
                    logger.error(f"[IPA AUDIO] Erro: {e}")
                break


# INICIALIZAÇÃO
if __name__ == "__main__":

    logger.info("Iniciando bot...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            handle_start
        )
    )

    app.add_handler(
        CommandHandler(
            "ipa",
            handle_ipa
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handle_ipa_audio_callback,
            pattern="^audio_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            handle_callback
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT,
            handle_text
        )
    )

    app.add_handler(
        MessageHandler(
            filters.VOICE,
            handle_audio
        )
    )

    logger.info(
        "Bot rodando e aguardando mensagens..."
    )

    app.run_polling()