from flask import Flask, request
import os
from telegram_bot import process_update
import requests
from config import TELEGRAM_TOKEN

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot DeFAI BSC activo 24/7 por Webhook"

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    process_update(request)
    return "ok", 200

def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/webhook/{TELEGRAM_TOKEN}"
    requests.post(url, data={"url": webhook_url})

if __name__ == "__main__":
    print("🚀 BOT DeFAI BSC INICIADO (MODO WEBHOOK GRATIS)")
    set_webhook()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
