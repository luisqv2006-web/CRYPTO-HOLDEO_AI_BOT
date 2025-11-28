from threading import Thread
from telegram_bot import start_telegram
from flask import Flask
import os

# =========================
# MINI SERVIDOR PARA RENDER (PUERTO FALSO)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot DeFAI BSC activo 24/7 (modo gratis)"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# =========================
# INICIO DEL SISTEMA
# =========================
if __name__ == "__main__":
    print("🚀 BOT DeFAI BSC INICIADO (MODO GRATIS CON PUERTO FALSO)")

    # Hilo para el servidor web (satisface a Render)
    Thread(target=run_web).start()

    # Bot de Telegram (lo importante)
    start_telegram()
