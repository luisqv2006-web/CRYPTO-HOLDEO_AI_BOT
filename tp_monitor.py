import requests
from positions_manager import get_open_positions, mark_tp_hit, close_position
from utils import get_klines
from main import send  # usamos la misma función de Telegram

def check_targets():
    positions = get_open_positions()

    for pos in positions:
        symbol = pos["symbol"]
        entry = pos["entry_price"]
        tp1 = pos["tp1"]
        tp2 = pos["tp2"]
        tp3 = pos["tp3"]

        # Obtener precio actual
        df = get_klines(symbol, "1d", 5)
        if df is None:
            continue
        
        price = df["close"].iloc[-1]

        # ==============================
        # TP1 — Recuperar liquidez
        # ==============================
        if price >= tp1 and not pos["tp1_hit"]:
            mark_tp_hit(symbol, "tp1_hit")
            send(f"""
🎯 *TP1 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
Precio: {price}
Estrategia recomendada:
• Vende ~30% para recuperar liquidez
• Mantén la posición mientras siga sobre EMA20D
""")

        # ==============================
        # TP2 — Tendencia en desarrollo
        # ==============================
        if price >= tp2 and not pos["tp2_hit"]:
            mark_tp_hit(symbol, "tp2_hit")
            send(f"""
📈 *TP2 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
Precio: {price}
Estrategia recomendada:
• Toma ganancias ~40%
• Mantén el resto para TP3 si estructura sigue fuerte
""")

        # ==============================
        # TP3 — Objetivo macro
        # ==============================
        if price >= tp3 and not pos["tp3_hit"]:
            mark_tp_hit(symbol, "tp3_hit")
            close_position(symbol)
            send(f"""
🚀 *TP3 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
Precio: {price}
Estrategia recomendada:
• Cerrar posición restante
• Esperar nueva acumulación
""")
