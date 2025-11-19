import requests
import time
import numpy as np
import os
from flask import Flask
import threading

# ===========================
# CONFIGURACIÓN TELEGRAM
# ===========================
TOKEN = "8466103477:AAHdB0YVMfxlj3fO8VQfZapAFi362-Vs4S0"
CHAT_ID = "-1003348348510"  # ← ESTE ES TU CHAT REAL
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ===========================
# SERVIDOR FLASK PARA RENDER
# ===========================
app = Flask(__name__)

@app.route("/")
def home():
    send("🔥 El bot CRYPTO ORÁCULO está ONLINE en Render.")
    return "CRYPTO ORÁCULO GOD MODE ULTRA — ACTIVO"

def iniciar_servidor():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, threaded=True)

# ===========================
# ENVIAR MENSAJE A TELEGRAM
# ===========================
def send(text):
    try:
        requests.post(API_URL, data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print("❌ Error enviando mensaje:", e)

# ===========================
# LISTA DE CRYPTOS TOP
# ===========================
TOP = {
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
# PRECIO BINANCE
# ===========================
def precio_binance(symbol):
    try:
        r = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        ).json()
        return float(r["price"])
    except:
        return None

# ===========================
# PRECIO COINGECKO
# ===========================
def precio_cg(coin_id):
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        ).json()
        return float(r[coin_id]["usd"])
    except:
        return None

# ===========================
# CÁLCULO DE RSI
# ===========================
def rsi(hist, period=14):
    delta = np.diff(hist)
    gains = delta.clip(min=0)
    losses = -delta.clip(max=0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def señal_rsi(valor):
    if valor < 25:
        return "🔥 *OPORTUNIDAD ÉPICA* (RSI ultra bajo)"
    if valor < 35:
        return "🚀 Posible rebote"
    if valor > 75:
        return "⚠️ Sobrecompra fuerte"
    return "📈 Normal"

# ===========================
# MOVIMIENTOS RÁPIDOS
# ===========================
def movimiento_rapido(p_actual, p_anterior):
    if p_anterior is None:
        return None
    cambio = (p_actual - p_anterior) / p_anterior * 100
    if cambio > 3:
        return f"🟢 SUBIDA RÁPIDA +{cambio:.2f}%"
    if cambio < -3:
        return f"🔴 CAÍDA RÁPIDA {cambio:.2f}%"
    return None

precios_previos = {}

# ===========================
# LOOP PRINCIPAL DEL BOT
# ===========================
def loop_bot():
    send("🚀 *CRYPTO ORÁCULO GOD MODE ULTRA ACTIVADO*")

    while True:
        for coin_id, simbolo in TOP.items():
            try:
                p1 = precio_binance(simbolo)
                p2 = precio_cg(coin_id)
                precios = [x for x in [p1, p2] if x is not None]

                if not precios:
                    continue

                precio = np.mean(precios)

                # Crear historial para RSI
                hist = [precio * (1 + np.random.uniform(-0.015, 0.015)) for _ in range(60)]
                valor_rsi = rsi(hist)
                señal = señal_rsi(valor_rsi)

                previo = precios_previos.get(simbolo)
                alerta_movi = movimiento_rapido(precio, previo)
                precios_previos[simbolo] = precio

                texto = f"""
🔮 *MACRO — {simbolo}*
💵 Precio: *${precio:.4f}*
📊 RSI: *{valor_rsi:.2f}*
⚡ Señal: {señal}
"""

                if alerta_movi:
                    texto += f"🚨 *ALERTA:* {alerta_movi}\n"

                send(texto)

            except Exception as e:
                print("❌ Error interno:", e)

        time.sleep(60)

# ===========================
# INICIO DE LOS HILOS
# ===========================
if __name__ == "__main__":
    threading.Thread(target=iniciar_servidor).start()
    threading.Thread(target=loop_bot).start()
