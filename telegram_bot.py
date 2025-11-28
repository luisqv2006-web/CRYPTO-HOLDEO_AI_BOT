from telegram.ext import Dispatcher, CommandHandler
from telegram import Bot, Update
from flask import request
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

def start(update, context):
    update.message.reply_text("✅ AHORA SÍ, BOT ACTIVO POR WEBHOOK 😎")

def test(update, context):
    update.message.reply_text("🧪 TEST OK — WEBHOOK FUNCIONANDO")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("test", test))

def process_update(req):
    update = Update.de_json(req.get_json(force=True), bot)
    dispatcher.process_update(update)
