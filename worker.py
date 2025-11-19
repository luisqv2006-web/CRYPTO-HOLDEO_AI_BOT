import time
import requests

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

# ================================
# CONFIGURACIÓN TELEGRAM FINAL
# ================================
TOKEN = "8466103477:AAHdB0YVMfxlj3fO8VQfZapAFi362-Vs4S0"
CHAT_ID = "-1009876543210"
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ================================
# CRYPTOS ACTIVAS
# ================================
CRYPTOS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "AVAXUSDT", "DOGEUSDT", "DOTUSDT", "LINKUSDT"
]

# ================================
# ANTI-CRASH
# ================================
def safe_value(v, decimals=2):
    try:
        return round(float(v), decimals)
    except:
        return 0

# ================================
# ENVIAR TELEGRAM
# ================================
def send(msg):
    try:
        requests.post(API_URL, data={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=5)
    except:
        pass

# ================================
# ANÁLISIS PRINCIPAL
# ================================
def analyze(symbol):
    df = get_klines(symbol, "1h", 200)
    if df is None:
        return

    try:
        # ===== INDICADORES =====
        e20 = safe_value(ema20(df).iloc[-1])
        e50 = safe_value(ema50(df).iloc[-1])
        e200 = safe_value(ema200(df).iloc[-1])

        rsi_val = safe_value(rsi(df).iloc[-1], 1)
        atr_val = safe_value(atr(df).iloc[-1], 3)
        mom = safe_value(momentum(df).iloc[-1])
        macd_line, signal_line, hist = macd(df)
        macd_hist = safe_value(hist.iloc[-1], 4)

        # ===== ESTRUCTURA DE MERCADO =====
        smc = smc_summary(df)

        # ===== IA =====
        ai = ai_score(df)

        # ===== NOTICIAS =====
        news = get_strong_news()

        # ===== BALLENAS =====
        whales = whale_monitor()

        # ===============================
        # MENSAJE FINAL PREMIUM (OPCIÓN 1)
        # ===============================
        msg = f"""
💎 *CRYPTO ORÁCULO VIP — {symbol}*
━━━━━━━━━━━━━━━━━━━━
📊 *Indicadores*
• EMA20: {e20}
• EMA50: {e50}
• EMA200: {e200}
• RSI: {rsi_val}
• ATR: {atr_val}
• Momentum: {mom}
• MACD hist: {macd_hist}

📉 *Smart Money Concepts*
{chr(10).join(smc)}

🔮 *IA Institucional*
• Confianza: {ai['confidence']}%
• ARIMA 1h: {ai['arima_1h']}
• ARIMA 4h: {ai['arima_4h']}
• LSTM: {ai['lstm']}

📰 *Noticias Importantes*
{chr(10).join([f"{n['icon']} {n['title']}" for n in news]) if news else 'Sin noticias relevantes.'}

🐳 *Ballenas*
{chr(10).join(whales) if whales else 'Sin movimientos importantes.'}
━━━━━━━━━━━━━━━━━━━━
"""

        send(msg)

    except Exception as e:
        send(f"⚠ Error analizando {symbol}: {str(e)[:80]}")


# ================================
# LOOP PRINCIPAL
# ================================
def loop():
    send("🚀 *WORKER INICIADO — Sistema institucional activado*")

    while True:
        for c in CRYPTOS:
            analyze(c)

        time.sleep(30)


if __name__ == "__main__":
    loop()
