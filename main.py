import logging
import time
import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)

from agents.orchestrator import handle_message
from audio.tts import speak


# Carrega variáveis .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


# Configuração de logs
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


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

        mensagem_texto, mensagem_audio = handle_message(
            user_text,
            user.id
        )


        logger.info("[FLOW] Gerando áudio (TTS)...")

        audio_file = speak(mensagem_audio)


        logger.info("[FLOW] Enviando resposta ao usuário...")

        await update.message.reply_text(
            mensagem_texto
        )

        await update.message.reply_voice(
            voice=open(audio_file, "rb")
        )


        elapsed = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"[SUCCESS] Resposta enviada em {elapsed}s"
        )

    except Exception as e:

        logger.error(
            f"[ERROR] Falha no handle_text: {e}"
        )

# ÁUDIO
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    start_time = time.time()

    user = update.effective_user

    logger.info(
        f"[AUDIO] Usuário: {user.id} enviou áudio"
    )

    try:

        logger.info("[FLOW] Baixando áudio...")

        file = await update.message.voice.get_file()

        file_path = "audio.ogg"

        await file.download_to_drive(file_path)


        logger.info("[FLOW] Transcrevendo áudio (STT)...")

        from audio.stt import transcribe

        texto = transcribe(file_path)

        logger.info(
            f"[STT] Texto transcrito: {texto}"
        )


        logger.info("[FLOW] Enviando para orquestrador...")

        mensagem_texto, mensagem_audio = handle_message(
            texto,
            user.id
        )


        logger.info("[FLOW] Gerando áudio (TTS)...")

        audio_file = speak(mensagem_audio)


        logger.info("[FLOW] Enviando resposta ao usuário...")

        await update.message.reply_text(
            f"Você disse: {texto}\n\n{mensagem_texto}"
        )

        await update.message.reply_voice(
            voice=open(audio_file, "rb")
        )


        elapsed = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"[SUCCESS] Áudio processado em {elapsed}s"
        )

    except Exception as e:

        logger.error(
            f"[ERROR] Falha no handle_audio: {e}"
        )

# INICIALIZAÇÃO
if __name__ == "__main__":

    logger.info("Iniciando bot...")

    app = ApplicationBuilder().token(TOKEN).build()

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