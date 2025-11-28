from threading import Thread
from telegram_bot import start_telegram
from flask import Flask
import os

# =========================
# MINI SERVIDOR PARA RENDER (PUERTO GRATIS)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot DeFAI BSC activo 24/7 (modo gratis)"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    # MUY IMPORTANTE: use_reloader=False evita el duplicado
    app.run(host="0.0.0.0", port=port, use_reloader=False)

# =========================
# INICIO ÚNICO DEL SISTEMA
# =========================
if __name__ == "__main__":
    print("🚀 BOT DeFAI BSC INICIADO (MODO GRATIS SIN DUPLICADOS)")

    Thread(target=run_web).start()

    # Solo UNA llamada real al bot de Telegram
    start_telegram()
