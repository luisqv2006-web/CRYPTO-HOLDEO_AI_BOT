import pandas as pd
import numpy as np

# ============================================================
#                SMART MONEY CONCEPTS (INSTITUCIONAL)
# ============================================================

def market_structure(df):
    close = df["close"]

    if close.iloc[-1] > close.iloc[-2] and close.iloc[-2] > close.iloc[-3]:
        return "📈 HH — Higher High"
    if close.iloc[-1] > close.iloc[-2] and close.iloc[-2] < close.iloc[-3]:
        return "📈 HL — Higher Low"
    if close.iloc[-1] < close.iloc[-2] and close.iloc[-2] > close.iloc[-3]:
        return "📉 LH — Lower High"
    if close.iloc[-1] < close.iloc[-2] and close.iloc[-2] < close.iloc[-3]:
        return "📉 LL — Lower Low"

    return "⚪ Estructura lateral"

def bos(df):
    close = df["close"]
    if close.iloc[-1] > close.iloc[-3]:
        return "🟢 BOS alcista"
    if close.iloc[-1] < close.iloc[-3]:
        return "🔴 BOS bajista"
    return None

def choch(df):
    c = df["close"]
    prev1 = c.iloc[-2] - c.iloc[-3]
    prev2 = c.iloc[-1] - c.iloc[-2]

    if prev1 < 0 and prev2 > 0:
        return "🟢 CHOCH — Alcista"
    if prev1 > 0 and prev2 < 0:
        return "🔴 CHOCH — Bajista"
    return None

def order_blocks(df):
    o = df["open"]
    c = df["close"]
    h = df["high"]
    l = df["low"]

    blocks = []

    if c.iloc[-1] > o.iloc[-1] and c.iloc[-2] < o.iloc[-2]:
        blocks.append(f"🟢 OB alcista ({l.iloc[-2]:.2f} - {o.iloc[-2]:.2f})")

    if c.iloc[-1] < o.iloc[-1] and c.iloc[-2] > o.iloc[-2]:
        blocks.append(f"🔴 OB bajista ({o.iloc[-2]:.2f} - {h.iloc[-2]:.2f})")

    return blocks if blocks else None

def fair_value_gaps(df):
    h = df["high"]
    l = df["low"]

    gaps = []

    if l.iloc[-1] > h.iloc[-3]:
        gaps.append("🟢 FVG alcista")

    if h.iloc[-1] < l.iloc[-3]:
        gaps.append("🔴 FVG bajista")

    return gaps if gaps else None

def liquidity_sweep(df):
    h = df["high"]
    l = df["low"]
    c = df["close"]

    if h.iloc[-1] > h.iloc[-3] and c.iloc[-1] < h.iloc[-1]:
        return "💧 Liquidez barrida arriba"

    if l.iloc[-1] < l.iloc[-3] and c.iloc[-1] > l.iloc[-1]:
        return "💧 Liquidez barrida abajo"

    return None

def liquidity_zones(df):
    max_zone = df["high"].rolling(20).max().iloc[-1]
    min_zone = df["low"].rolling(20).min().iloc[-1]
    return max_zone, min_zone

def smc_summary(df):
    summary = []

    b = bos(df)
    if b: summary.append(b)

    c = choch(df)
    if c: summary.append(c)

    ob = order_blocks(df)
    if ob: summary.extend(ob)

    fvg = fair_value_gaps(df)
    if fvg: summary.extend(fvg)

    sweep = liquidity_sweep(df)
    if sweep: summary.append(sweep)

    struct = market_structure(df)
    if struct: summary.append(struct)

    return summary if summary else ["⚪ Sin eventos SMC"]
