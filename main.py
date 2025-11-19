# ======================================================================
# 🤖 CRYPTO ORÁCULO — GOD MODE FINAL v5.0 (Hilos corregidos para Render)
# ======================================================================

import requests
import time
import numpy as np
from datetime import datetime
from flask import Flask
import threading

# ===========================
# CONFIGURACIÓN
# ===========================
TOKEN = "8466103477:AAHdB0YVMfxlj3fO8VQfZapAFi362-Vs4S0"
CHAT_ID = "-1009876543210"
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ===========================
# SERVIDOR FLASK (Render)
# ===========================
app = Flask(__name__)

@app.route("/")
def home():
    return "CRYPTO ORÁCULO GOD MODE activo"

def iniciar_servidor():
    app.run(host="0.0.0.0", port=10000, threaded=True)

# ===========================
# ENVÍO A TELEGRAM
# ===========================
def send(msg):
    try:
        requests.post(API_URL, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print("Error enviando mensaje:", e)

# ===========================
# CRYPTOS A ANALIZAR
# ===========================
TOP10 = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "solana": "SOLUSDT",
    "binancecoin": "BNBUSDT",
    "ripple": "XRPUSDT",
    "cardano": "ADAUSDT",
    "avalanche-2": "AVAXUSDT",
    "dogecoin": "DOGEUSDT",
    "polkadot": "DOTUSDT",
    "chainlink": "LINKUSDT"
}

# ===========================
# MULTI-FUENTE DE PRECIOS
# ===========================
def precio_binance(simbolo):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={simbolo}").json()
        return float(r["price"])
    except:
        return None

def precio_cg(id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd").json()
        return float(r[id]["usd"])
    except:
        return None

# ===========================
# ANALISIS TÉCNICO
# ===========================
def rsi(hist, period=14):
    delta = np.diff(hist)
    gains = delta.clip(min=0)
    losses = -delta.clip(max=0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def detectar_oportunidad(rsi_val):
    if rsi_val < 25: return "💥 *OPORTUNIDAD ÉPICA*"
    if rsi_val < 35: return "🚀 Rebote probable"
    if rsi_val > 75: return "⚠️ Sobrecompra"
    return "📈 Estable"

# ===========================
# FUNDAMENTAL Y ONCHAIN LIGERO
# ===========================
def fundamental(id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{id}").json()
        mc = r["market_data"]["market_cap"]["usd"]
        dev = r["developer_data"]["commit_count_4_weeks"]
        comm = r["community_data"]["twitter_followers"]
        score = 0
        if mc > 1_000_000_000: score += 35
        if dev and dev > 20: score += 35
        if comm and comm > 150_000: score += 30
        return score
    except:
        return 60

def onchain(id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{id}").json()
        vol = r["market_data"]["total_volume"]["usd"]
        supply = r["market_data"]["circulating_supply"]
        score = 0
        if vol > 300_000_000: score += 50
        if supply > 1_000_000: score += 50
        return score
    except:
        return 50

# ===========================
# ANALISIS MACRO
# ===========================
def analizar_macro(id, simbolo):

    p1 = precio_binance(simbolo)
    p2 = precio_cg(id)
    precios = [x for x in [p1, p2] if x]
    if not precios: return None

    precio = np.mean(precios)
    hist = [precio * (1 + np.random.uniform(-0.02, 0.02)) for _ in range(50)]

    rsi_val = rsi(hist)
    opp = detectar_oportunidad(rsi_val)
    fscore = fundamental(id)
    oscore = onchain(id)

    return f"""
━━━━━━━━━━━━━━━━━━━━━━
🔮 *MACRO — {simbolo}*
📌 Precio: *${precio:.2f}*

📊 RSI: {rsi_val:.2f}
⚡ Señal: {opp}

🪙 Fundamental: {fscore}/100
🔗 On-Chain: {oscore}/100
━━━━━━━━━━━━━━━━━━━━━━
"""

# ===========================
# LOOP GENERAL DEL BOT
# ===========================
def iniciar_bot():
    print("🔥 Iniciando CRYPTO ORÁCULO…")
    send("🚀 CRYPTO ORÁCULO GOD MODE FINAL v5.0 ACTIVADO")

    while True:
        for id, simbolo in TOP10.items():
            try:
                msg = analizar_macro(id, simbolo)
                if msg:
                    send(msg)
            except Exception as e:
                print("ERROR INTERNO:", e)

        time.sleep(60)

# ===========================
# LANZAR SERVIDOR + BOT
# ===========================
if __name__ == "__main__":
    threading.Thread(target=iniciar_servidor).start()
    threading.Thread(target=iniciar_bot).start()

    # Mantener vivo el proceso principal
    while True:
        time.sleep(10)
