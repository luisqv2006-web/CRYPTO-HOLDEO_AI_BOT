from telegram.ext import Updater, CommandHandler
from scanner import scan_farms
from farmer import enter_farm, farm_status, exit_farm
from config import TELEGRAM_TOKEN, CHAT_ID

bot_active = False

def start(update, context):
    update.message.reply_text("🤖 Bot DeFAI BSC activo.")

def estado(update, context):
    farm, rewards = farm_status()
    if farm:
        update.message.reply_text(f"🌾 Farm: {farm['pair']}\nRewards: {round(rewards,2)} USD")
    else:
        update.message.reply_text("⏸ No hay farming activo.")

def activar(update, context):
    global bot_active
    bot_active = True
    farms = scan_farms()
    respuesta = enter_farm(farms[0])
    update.message.reply_text(respuesta)

def salir(update, context):
    update.message.reply_text(exit_farm())

def panico(update, context):
    update.message.reply_text("🚨 MODO PÁNICO ACTIVADO\n" + exit_farm())

def start_telegram():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("estado", estado))
    dp.add_handler(CommandHandler("activar", activar))
    dp.add_handler(CommandHandler("salir", salir))
    dp.add_handler(CommandHandler("panico", panico))

    updater.start_polling()
    updater.idle()
