from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN

def start(update, context):
    update.message.reply_text("✅ AHORA SÍ, BOT VIVO Y SIN CONFLICTOS 😎")

def test(update, context):
    update.message.reply_text("🧪 TEST OK — SESIÓN ÚNICA ACTIVA")

def start_telegram():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))

    # Esto limpia mensajes atorados de sesiones viejas
    updater.start_polling(drop_pending_updates=True)
    updater.idle()
