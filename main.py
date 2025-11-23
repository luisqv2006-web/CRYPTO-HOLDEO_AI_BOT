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
from indicators import (
    ema20, ema50, ema200, rsi,
    detect_divergence
)
from smc import smc_summary
from machine_learning import ai_score
from sentiment import get_strong_news
from whales import whale_monitor
from positions_manager import add_position
from tp_monitor import check_targets


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
# FUNCIONES DE CÁLCULO
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
    tp1 = precio + abs(precio * stop_pct)     # Recuperar liquidez
    tp2 = precio * 1.35                       # Tendencia
    tp3 = precio * 2.0                        # Macro
    return tp1, tp2, tp3


# ============================================
# PUNTAJE DE OPORTUNIDAD PARA HOLDEO
# ============================================

def puntaje_holdeo(df, symbol):
    score = 0
    razones = []

    precio = df["close"].iloc[-1]
    e200 = ema200(df).iloc[-1]
    rsi_v = rsi(df).iloc[-1]
    div = detect_divergence(df)

    # Precio bajo EMA200 = descuento institucional
    if precio < e200:
        score += 2
        razones.append("📉 Precio bajo EMA200 — Descuento institucional")

    # RSI bajo
    if rsi_v < 35:
        score += 2
        razones.append("🔻 RSI en zona de sobreventa")

    # Divergencia
    if div:
        score += 1
        razones.append(f"⚠ {div}")

    # IA de predicción
    ai = ai_score(df)
    if ai["confidence"] > 65:
        score += 2
        razones.append(f"🤖 IA proyecta subida ({ai['confidence']}%)")

    # Ballenas
    whales = whale_monitor()
    if whales:
        score += 2
        razones.append("🐳 Acumulación de ballenas")

    return score, razones


# ============================================
# ENVÍO DE ALERTA + REGISTRO DE POSICIÓN
# ============================================

def enviar_alerta(symbol, score, razones, monto_info, tp1, tp2, tp3):
    precio = monto_info["precio"]
    sugerido = monto_info["monto"]
    riesgo = monto_info["riesgo"]

    # 🔥 Registrar posición automáticamente
    add_position(
        symbol=symbol,
        entry_price=precio,
        amount=sugerido,
        tp1=tp1,
        tp2=tp2,
        tp3=tp3
    )

    msg = f"""
💎 *OPORTUNIDAD DE HOLDEO — {symbol}*
━━━━━━━━━━━━━━━━━━━━
📍 Precio actual: {precio}

📊 *Puntaje:* {score}/10  
💰 *Compra sugerida:* ${sugerido} MXN  
⚠ *Riesgo:* ${riesgo} MXN (2%)

🔍 *Razones institucionales:*
{chr(10).join(razones)}

🎯 *Take Profits planificados*
• TP1: {tp1:.2f} — Recuperar liquidez
• TP2: {tp2:.2f} — Tendencia
• TP3: {tp3:.2f} — Macro / salida final

🧭 *Estrategia paso a paso*
1️⃣ Compra la cantidad sugerida
2️⃣ Mantén mientras el precio siga sobre EMA20D
3️⃣ Reduce si rompe estructura
4️⃣ Vende parcial en TP1/TP2
5️⃣ Cierra ciclo en TP3

📌 Entrada registrada automáticamente.
━━━━━━━━━━━━━━━━━━━━
"""
    send(msg)


# ============================================
# ANÁLISIS PRINCIPAL
# ============================================

def analizar_symbol(symbol):
    df = get_klines(symbol, "1d", 200)
    if df is None:
        return

    score, razones = puntaje_holdeo(df, symbol)

    if score >= UMBRAL_SENAL:
        precio = df["close"].iloc[-1]
        stop_pct = 0.09

        monto_info = calcular_monto(precio, stop_pct)
        tp1, tp2, tp3 = calcular_tps(precio, stop_pct)

        enviar_alerta(symbol, score, razones, monto_info, tp1, tp2, tp3)


# ============================================
# LOOP PRINCIPAL
# ============================================

def analizar():
    send("🚀 *Modo Holdeo Activado — Señales solo con confluencias fuertes*")

    while True:
        for symbol in CRYPTOS:
            analizar_symbol(symbol)

        # Revisión de TPs alcanzados
        check_targets()

        time.sleep(3600)  # Analiza cada hora


# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    analizar()
