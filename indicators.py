import numpy as np
import pandas as pd

# ============================================================
#                 INDICADORES INSTITUCIONALES
# ============================================================

# ---------------------- EMA ---------------------------------
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def ema20(df):
    return ema(df["close"], 20)

def ema50(df):
    return ema(df["close"], 50)

def ema200(df):
    return ema(df["close"], 200)

# ---------------------- RSI PRO -------------------------------
def rsi(df, period=14):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))

# ---------------------- VOLATILIDAD REAL ----------------------
def true_range(df):
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        abs(df["high"] - prev_close),
        abs(df["low"] - prev_close)
    ], axis=1).max(axis=1)
    return tr

def atr(df, period=14):
    tr = true_range(df)
    return tr.rolling(period).mean()

# ---------------------- MOMENTUM -------------------------------
def momentum(df, period=10):
    return df["close"] - df["close"].shift(period)

# ---------------------- MACD PRO -------------------------------
def macd(df):
    ema12 = ema(df["close"], 12)
    ema26 = ema(df["close"], 26)
    macd_line = ema12 - ema26
    signal_line = ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# ---------------------- VOLUMEN -------------------------------
def volume_change(df):
    vol = df["volume"]
    return (vol - vol.shift(1)) / vol.shift(1) * 100

# ---------------------- DIVERGENCIAS --------------------------
def detect_divergence(df):
    r = rsi(df).fillna(0)
    price = df["close"]

    div = None

    if price.iloc[-1] < price.iloc[-3] and r.iloc[-1] > r.iloc[-3]:
        div = "🔵 Divergencia Alcista"

    if price.iloc[-1] > price.iloc[-3] and r.iloc[-1] < r.iloc[-3]:
        div = "🔴 Divergencia Bajista"

    return div

# ---------------------- PATRONES DE VELAS ----------------------
def candle_pattern(df):
    o = df["open"].iloc[-1]
    h = df["high"].iloc[-1]
    l = df["low"].iloc[-1]
    c = df["close"].iloc[-1]

    prev_o = df["open"].iloc[-2]
    prev_c = df["close"].iloc[-2]

    if abs(c - o) <= (h - l) * 0.1:
        return "⚫ Doji — indecisión"

    if (o - l) > (h - o) * 2 and (c - l) > (h - c) * 2:
        return "🔨 Martillo alcista"

    if c > o and prev_c < prev_o and c > prev_o and o < prev_c:
        return "🟢 Engulfing Alcista"

    if c < o and prev_c > prev_o and o > prev_c and c < prev_o:
        return "🔴 Engulfing Bajista"

    return None

# ---------------------- FUERZA DE TENDENCIA --------------------
def trend_strength(df):
    e20 = ema20(df)
    e50 = ema50(df)

    if e20.iloc[-1] > e50.iloc[-1]:
        return "📈 Tendencia Alcista"
    if e20.iloc[-1] < e50.iloc[-1]:
        return "📉 Tendencia Bajista"

    return "⚪ Lateral"

# ---------------------- ZONAS SENSIBLES ------------------------
def price_zones(df):
    max_price = df["high"].rolling(20).max().iloc[-1]
    min_price = df["low"].rolling(20).min().iloc[-1]
    return max_price, min_price
