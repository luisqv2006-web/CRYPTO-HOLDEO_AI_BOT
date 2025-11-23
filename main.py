# ============================================
# CRYPTOSNIPER HOLD — ANALISTA INSTITUCIONAL
# Modo Holdeo | Señales + Registro + Seguimiento
# ============================================

import time
import requests
import numpy as np
import os
from dotenv import load_dotenv

# ==== Importar módulos auxiliares ====
from utils import get_klines
from indicators import ema20, ema50, ema200, rsi, detect_divergence
from smc import smc_summary
from machine_learning import ai_score
from sentiment import get_strong_news
from whales import whale_monitor
from positions_manager import add_position
import tp_monitor


# ============================================
# CONFIGURACIÓN
# ============================================

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CAPITAL_TOTAL = int(os.getenv("CAPITAL", 500))
RIESGO = 0.02  # 2%
UMBRAL_SENAL = 6

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


# ============================================
# LISTA DE CRYPTOS A ANALIZAR
# ============================================

CRYPTOS = [
    "BTCUSDT", "ETHUSDT",
    "SOLUSDT", "BNBUSDT", "AVAXUSDT", "ADAUSDT",
    "DOTUSDT", "ATOMUSDT",
    "OPUSDT", "ARBUSDT", "SUIUSDT", "SEIUSDT", "INJUSDT",
    "RNDRUSDT", "FETUSDT", "TAOUSDT"
]


# ============================================
# FUNCIÓN PARA ENVIAR MENSAJES A TELEGRAM
# ============================================

def send(msg):
    requests.post(API_URL, data={
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    })


# ============================================
# PUNTAJE HOLDEO (ANTICRASH)
# ============================================

def puntaje_holdeo(df, symbol):

    # 🔰 1. Validación fuerte para evitar crashes
    if df is None or not hasattr(df, "empty") or df.empty:
        print(f"[ERROR] DF vacío para {symbol}")
        return 0, ["❌ Datos insuficientes"]

    if "close" not in df.columns or len(df["close"]) < 2:
        print(f"[ERROR] DF sin columna close válida para {symbol}")
        return 0, ["❌ Velas insuficientes"]

    score = 0
    razones = []

    # === Datos seguros ===
    try:
        precio = df["close"].iloc[-1]
    except:
        return 0, ["❌ No se pudo obtener precio"]

    # === Indicadores ===
    try:
        e200 = ema200(df).iloc[-1]
    except:
        e200 = precio

    try:
        rsi_v = rsi(df).iloc[-1]
    except:
        rsi_v = 50

    div = detect_divergence(df)

    # === Reglas ===
    if precio < e200:
        score += 2
        razones.append("📉 Precio bajo EMA200 — Descuento institucional")

    if rsi_v < 35:
        score += 2
        razones.append("🔻 RSI sobreventa")

    if div:
        score += 1
        razones.append(f"⚠ {div}")

    # IA
    ia = ai_score(df)
    if ia and ia.get("confidence", 0) > 65:
        score += 2
        razones.append(f"🤖 IA: {ia['confidence']}% confianza")

    # Ballenas
    whales = whale_monitor()
    if whales:
        score += 2
        razones.append("🐳 Acumulación de ballenas")

    return score, razones


# ============================================
# CÁLCULOS DINÁMICOS
# ============================================

def calcular_monto(precio, stop_pct, capital=CAPITAL_TOTAL, riesgo_pct=RIESGO):
    riesgo = capital * riesgo_pct
    perdida_unidad = precio * stop_pct
    monto = riesgo / perdida_unidad

    return {
        "precio": precio,
        "riesgo": riesgo,
        "monto": round(monto, 2),
        "stop_pct": stop_pct
    }


def calcular_tps(precio, stop_pct):
    tp1 = precio + abs(precio * stop_pct)
    tp2 = precio * 1.35
    tp3 = precio * 2.0
    return tp1, tp2, tp3


# ============================================
# ANALIZAR SYMBOL
# ============================================

def analizar_symbol(symbol):
    df = get_klines(symbol, "1d", 200)

    if df is None or not hasattr(df, "empty") or df.empty:
        print(f"[SKIP] No data for {symbol}")
        return

    score, razones = puntaje_holdeo(df, symbol)

    if score < UMBRAL_SENAL:
        return

    precio = df["close"].iloc[-1]
    stop_pct = 0.09

    monto_info = calcular_monto(precio, stop_pct)
    tp1, tp2, tp3 = calcular_tps(precio, stop_pct)

    enviar_alerta(symbol, score, razones, monto_info, tp1, tp2, tp3)


# ============================================
# ALERTA
# ============================================

def enviar_alerta(symbol, score, razones, monto_info, tp1, tp2, tp3):

    add_position(
        symbol=symbol,
        entry_price=monto_info["precio"],
        amount=monto_info["monto"],
        tp1=tp1, tp2=tp2, tp3=tp3
    )

    msg = f"""
💎 *OPORTUNIDAD DE HOLDEO — {symbol}*
━━━━━━━━━━━━━━━━━━━━
📍 Precio actual: {monto_info['precio']}

📊 *Puntaje:* {score}/10  
💰 *Compra sugerida:* ${monto_info['monto']} MXN  
⚠ *Riesgo:* ${monto_info['riesgo']} MXN

🔍 *Razones:*
{chr(10).join(razones)}

🎯 *Take Profits*
• TP1: {tp1:.2f}
• TP2: {tp2:.2f}
• TP3: {tp3:.2f}

📌 Entrada registrada automáticamente.
━━━━━━━━━━━━━━━━━━━━
"""
    send(msg)


# ============================================
# LOOP PRINCIPAL
# ============================================

def analizar():
    send("🚀 *Modo Holdeo Activado*")

    while True:
        for symbol in CRYPTOS:
            analizar_symbol(symbol)

        tp_monitor.check_targets()
        time.sleep(3600)



# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    analizar()
