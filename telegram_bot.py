from telegram.ext import Updater, CommandHandler
from config import TELEGRAM_TOKEN

def start(update, context):
    update.message.reply_text("✅ RESPONDO PERFECTO DESDE RENDER 😎")

def test(update, context):
    update.message.reply_text("🧪 TEST OK — EL BOT SÍ ESTÁ VIVO")

def start_telegram():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", test))

    updater.start_polling()
    updater.idle()
