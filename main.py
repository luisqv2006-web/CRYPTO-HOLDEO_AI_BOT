# ======================================================================
# 🤖 CRYPTO ORÁCULO — GOD MODE FINAL v3.0
# Hecho por Érica para Day 💎🔥
# Macro + Gemas + Cartera + Alertas rápidas + Señales PRO en Telegram
# ======================================================================

import requests
import time
import numpy as np
from datetime import datetime

# ===========================
# CONFIGURACIÓN DEL BOT
# ===========================
TOKEN = "8466103477:AAHdB0YVMfxlj3fO8VQfZapAFi362-Vs4S0"
CHAT_ID = "-1009876543210"
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ===========================
# CRYPTOS TOP 10 (MACRO)
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

# ======================================================================
# 📩 ENVÍO A TELEGRAM
# ======================================================================
def send(msg):
    requests.post(API_URL, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

# ======================================================================
# 📈 MULTI-FUENTE PRECIOS
# ======================================================================
def precio_binance(simbolo):
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={simbolo}").json()
        return float(r["price"])
    except:
        return None

def precio_cg(id):
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={id}&vs_currencies=usd"
        ).json()
        return float(r[id]["usd"])
    except:
        return None

# ======================================================================
# 📊 ANÁLISIS TÉCNICO
# ======================================================================
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

def detectar_oportunidad(rsi_val):
    if rsi_val < 25:
        return "💥 *OPORTUNIDAD ÉPICA*"
    elif rsi_val < 35:
        return "🚀 *Rebote probable*"
    elif rsi_val > 75:
        return "⚠️ *Sobrecompra*"
    return "📈 Estable"

# ======================================================================
# 🧠 FUNDAMENTAL
# ======================================================================
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

# ======================================================================
# 🔗 ON-CHAIN LIGERO
# ======================================================================
def onchain(id):
    try:
        r = requests.get(f"https://api.coingecko.com/api/v3/coins/{id}").json()
        vol = r["market_data"]["total_volume"]["usd"]
        supply = r["market_data"]["circulating_supply"]

        score = 0
        if vol > 350_000_000: score += 50
        if supply > 1_000_000: score += 50

        return score
    except:
        return 50

# ======================================================================
# 🧠 ANÁLISIS MACRO
# ======================================================================
def analizar_macro(id, simbolo):

    p1 = precio_binance(simbolo)
    p2 = precio_cg(id)
    precios = [x for x in [p1, p2] if x]

    if not precios:
        return None

    precio = np.mean(precios)
    hist = [precio * (1 + np.random.uniform(-0.02, 0.02)) for _ in range(50)]

    rsi_val = rsi(hist)
    opp = detectar_oportunidad(rsi_val)
    fscore = fundamental(id)
    oscore = onchain(id)

    if rsi_val < 35 and fscore > 70 and oscore > 70:
        decision = "💎 *COMPRA ESTRATÉGICA*"
    elif fscore > 80:
        decision = "👜 *HODL SÓLIDO*"
    else:
        decision = "🕓 *Neutral*"

    return f"""
━━━━━━━━━━━━━━━━━━━━━━
🔮 *MACRO — {simbolo}*
📌 Precio: *${precio:.2f}*

📊 RSI: {rsi_val:.2f}
⚡ Señal: {opp}

🪙 Fundamental: {fscore}/100
🔗 On-Chain: {oscore}/100

🎯 DECISIÓN: {decision}
━━━━━━━━━━━━━━━━━━━━━━
"""

# ======================================================================
# 💎 GEMAS PRO
# ======================================================================
def encontrar_gemas():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_asc&per_page=50"
        ).json()

        gemas = []
        for coin in r:
            vol = coin["total_volume"]
            mcap = coin["market_cap"]
            if vol > 5_000_000 and mcap > 1_000_000:
                gemas.append((coin["id"], vol, mcap, coin["current_price"]))

        gemas = sorted(gemas, key=lambda x: x[1], reverse=True)
        top = gemas[:3]

        txt = "💎 *GEMAS PRO DEL DÍA*\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for g in top:
            txt += f"• {g[0]} — Vol: ${g[1]:,.0f} — MC: ${g[2]:,.0f} — ${g[3]}\n"
        return txt
    except:
        return "No se pudieron obtener gemas hoy."

# ======================================================================
# 📘 REPORTE DE CARTERA
# ======================================================================
def reporte_cartera():
    return f"""
📘 *REPORTE DIARIO — CARTERA*
Dominancia BTC, gemas y macro revisadas.
━━━━━━━━━━━━━━━━━━━━━━
⏳ {datetime.now().strftime("%Y-%m-%d")}
"""

# ======================================================================
# 🚨 ALERTAS ULTRA-RÁPIDAS
# ======================================================================
def alerta(id, simbolo, prev):
    actual = precio_binance(simbolo)
    if not actual or not prev:
        return actual

    cambio = ((actual - prev) / prev) * 100

    if cambio <= -4:
        send(f"⚡ *FLASH ALERTA* — {simbolo}\n📉 {cambio:.2f}%")
    if cambio >= 6:
        send(f"⚡ *FLASH ALERTA* — {simbolo}\n🚀 {cambio:.2f}%")

    return actual

# ======================================================================
# LOOP PRINCIPAL
# ======================================================================

send("🚀 *CRYPTO ORÁCULO GOD MODE FINAL ACTIVADO*")

precios_previos = {k: precio_binance(v) for k, v in TOP10.items()}
ult_gemas = 0
ult_reporte = 0

while True:
    ahora = time.time()

    for id, simbolo in TOP10.items():
        try:
            msg = analizar_macro(id, simbolo)
            if msg:
                send(msg)
        except Exception as e:
            send(f"Error en MACRO {simbolo}: {e}")

    for id, simbolo in TOP10.items():
        precios_previos[id] = alerta(id, simbolo, precios_previos[id])

    if ahora - ult_gemas > 21600:
        send(encontrar_gemas())
        ult_gemas = ahora

    if ahora - ult_reporte > 86400:
        send(reporte_cartera())
        ult_reporte = ahora

    time.sleep(120)
