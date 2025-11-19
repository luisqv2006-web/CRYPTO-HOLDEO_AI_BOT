# ------------------------------------
# CRYPTOSNIPER FX — ULTRA PRO BINARIAS v4.0 (STAKE $5)
# ------------------------------------
from keep_alive import keep_alive
keep_alive()

import time
import requests
import threading
import statistics
import pytz
from datetime import datetime

from auto_copy import AutoCopy

# ------------------------------------
# CONFIGURACIÓN
# ------------------------------------
TOKEN = "8588736688:AAF_mBkQUJIDXqAKBIzgDvsEGNJuqXJHNxA"
CHAT_ID = "-1003348348510"
DERIV_TOKEN = "z30pnK3N1UjKZTA"

FINNHUB_KEY = "d4d2n71r01qt1lahgi60d4d2n71r01qt1lahgi6g"
NEWS_API = f"https://finnhub.io/api/v1/calendar/economic?token={FINNHUB_KEY}"

API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

mx = pytz.timezone("America/Mexico_City")

# ------------------------------------
# ACTIVOS (Deriv Symbols)
# ------------------------------------
SYMBOLS = {
    "XAU/USD": "frxXAUUSD",
    "EUR/USD": "frxEURUSD",
    "GBP/USD": "frxGBPUSD",
    "USD/JPY": "frxUSDJPY"
}

# Inicializar AutoCopy (sin monto aquí, lo mandamos en cada señal)
copy_trader = AutoCopy(DERIV_TOKEN)

# ------------------------------------
# MENSAJERÍA TELEGRAM
# ------------------------------------
def send(msg):
    try:
        requests.post(API, json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        })
    except:
        pass


# ------------------------------------
# OBTENER VELAS 5M
# ------------------------------------
def obtener_velas_5m(symbol_key):
    symbol = SYMBOLS[symbol_key]
    now = int(time.time())
    desde = now - (60 * 60 * 12)

    url = (
        f"https://finnhub.io/api/v1/forex/candle?"
        f"symbol={symbol}&resolution=5&from={desde}&to={now}&token={FINNHUB_KEY}"
    )

    r = requests.get(url).json()
    if r.get("s") != "ok":
        return None

    return list(zip(r["t"], r["o"], r["h"], r["l"], r["c"]))


# ------------------------------------
# DETECCIÓN ICT PRO ULTRA
# ------------------------------------
def detectar_confluencias(velas):
    o,h,l,c = zip(*[(x[1], x[2], x[3], x[4]) for x in velas[-12:]])

    cons = {
        "BOS": False,
        "CHOCH": False,
        "OrderBlock": False,
        "FVG_Internal": False,
        "FVG_External": False,
        "EQH": False,
        "EQL": False,
        "Liquidity_Internal": False,
        "Liquidity_External": False,
        "Volatilidad": False,
        "Tendencia": False
    }

    if c[-1] > h[-2]: cons["BOS"] = True
    if c[-1] < l[-2]: cons["CHOCH"] = True

    if (c[-1] > o[-1] and l[-1] > l[-2]) or (c[-1] < o[-1] and h[-1] < h[-2]):
        cons["OrderBlock"] = True

    if h[-2
