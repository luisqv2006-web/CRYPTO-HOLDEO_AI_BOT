import time
import requests
import numpy as np
import hashlib
import hmac
import urllib.parse

from utils import get_klines
from indicators import (
    ema20, ema50, ema200, rsi, atr, momentum, macd,
    detect_divergence, candle_pattern, volume_change,
    trend_strength, price_zones
)
from smc import smc_summary
from machine_learning import ai_score
from sentiment import get_strong_news
from whales import whale_monitor


# ======================================================
# 🔥 TELEGRAM CONFIG — DATOS REALES
# ======================================================
TOKEN = "8466103477:AAHdB0YVMfxlj3fO8VQfZapAFi362-Vs4S0"
CHAT_ID = "-1003348348510"
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# ======================================================
# 🔥 BINANCE CONFIG (LECTURA DE MERCADO)
# ======================================================
API_KEY = ""       # No obligatorio para datos públicos
API_SECRET = ""    # No obligatorio para datos públicos
BASE_URL = "https://api.binance.com"


def binance_request(endpoint, params=None):
    url = BASE_URL + endpoint
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=5)
        return r.json()
    except:
        return None


# ======================================================
# 🔥 LISTA DE CRYPTOS VIP
# ======================================================
CRYPTOS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT",
    "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT",
    "DOTUSDT", "LINKUSDT"
]


# ======================================================
# 📩 ENVIAR A TELEGRAM
# ======================================================
def send(msg):
    try:
        requests.post(API_URL, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=5)
    except:
        pass


# ======================================================
# 🔥 ANÁLISIS PROFESIONAL (VIP)
# ======================================================
def analyze(symbol):
    df = get_klines(symbol, "1h", 200)
    if df is None or len(df) < 200:
        return

    try:
        # INDICADORES TÉCNICOS
        e20 = ema20(df).iloc[-1]
        e50 = ema50(df).iloc[-1]
        e200 = ema200(df).iloc[-1]
        rsi_v = rsi(df).iloc[-1]
        atr_v = atr(df).iloc[-1]
        mom = momentum(df).iloc[-1]
        macd_line, signal, hist = macd(df)

        # SMART MONEY CONCEPTS
        smc = smc_summary(df)

        # PATRONES / DIVERGENCIAS
        div = detect_divergence(df)
        candle = candle_pattern(df)
        vol = volume_change(df)
        trend = trend_strength(df)
        max_z, min_z = price_zones(df)

        # IA
        ai = ai_score(df)

        # NOTICIAS
        news = get_strong_news()

        # BALLENAS
        whales = whale_monitor()

        # MENSAJE VIP FINAL
        msg = f"""
💎 *CRYPTOHOLDEO_AI_VIP — {symbol}*
━━━━━━━━━━━━━━━━━━━━
📊 *Indicadores*
• EMA20: {e20:.2f}
• EMA50: {e50:.2f}
• EMA200: {e200:.2f}
• RSI: {rsi_v:.1f}
• ATR: {atr_v:.3f}
• Momentum: {mom:.2f}
• MACD hist: {hist.iloc[-1]:.4f}

📉 *Smart Money Concepts*
{chr(10).join(smc)}

📈 *Liquidez*
• Zona alta: {max_z:.2f}
• Zona baja: {min_z:.2f}

🔍 *Patrones*
• Divergencia: {div}
• Velas: {candle}
• Volumen: {vol}
• Tendencia: {trend}

🤖 *IA*
• Confianza: {ai['confidence']}%
• ARIMA 1h: {ai['arima_1h']}
• ARIMA 4h: {ai['arima_4h']}
• LSTM: {ai['lstm']}

📰 *Noticias*
{chr(10).join([f"{n['icon']} {n['title']}" for n in news]) if news else 'Sin noticias importantes.'}

🐳 *Ballenas*
{chr(10).join(whales) if whales else 'Sin movimientos grandes.'}
━━━━━━━━━━━━━━━━━━━━
"""

        send(msg)

    except Exception as e:
        send(f"⚠️ Error analizando {symbol}: {str(e)[:80]}")


# ======================================================
# 🔁 LOOP PRINCIPAL
# ======================================================
def loop():
    send("🚀 *WORKER VIP ACTIVADO — Señales institucionales en tiempo real*")

    while True:
        for c in CRYPTOS:
            analyze(c)

        time.sleep(60)


# ======================================================
# ▶️ EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    loop()
