import requests
from positions_manager import get_open_positions, mark_tp_hit, close_position
from utils import get_klines


# ============================================
# VERIFICAR OBJETIVOS DE TAKE PROFIT
# ============================================

def check_targets():
    positions = get_open_positions()

    if not positions:
        return  # nada que revisar

    for pos in positions:
        symbol = pos["symbol"]
        tp1 = pos["tp1"]
        tp2 = pos["tp2"]
        tp3 = pos["tp3"]

        # Obtener precio actual (usa timeframes largos)
        df = get_klines(symbol, "1d", 50)
        if df is None or df.empty:
            continue
        
        price = df["close"].iloc[-1]

        # ==============================
        # TP1 — Recuperar liquidez
        # ==============================
        if price >= tp1 and not pos["tp1_hit"]:
            mark_tp_hit(symbol, "tp1_hit")
            send_tp_alert(symbol, price, 1)

        # ==============================
        # TP2 — Tendencia
        # ==============================
        if price >= tp2 and not pos["tp2_hit"]:
            mark_tp_hit(symbol, "tp2_hit")
            send_tp_alert(symbol, price, 2)

        # ==============================
        # TP3 — Cierre total
        # ==============================
        if price >= tp3 and not pos["tp3_hit"]:
            mark_tp_hit(symbol, "tp3_hit")
            close_position(symbol)
            send_tp_alert(symbol, price, 3)


# ============================================
# MENSAJES AL USUARIO
# ============================================

def send_tp_alert(symbol, price, target):
    from main import send  # importar dentro para evitar errores circulares

    if target == 1:
        msg = f"""
🎯 *TP1 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
📌 Precio: {price}
📍 Recomendación: vender ~30% para recuperar liquidez.
Sigue mientras mantenga soporte.
"""
    elif target == 2:
        msg = f"""
📈 *TP2 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
📌 Precio: {price}
📍 Recomendación: tomar ~40% de ganancias.
Mantén restante para TP3 si sigue con fuerza.
"""
    elif target == 3:
        msg = f"""
🚀 *TP3 ALCANZADO — {symbol}*
━━━━━━━━━━━━━━━━━━
📌 Precio: {price}
📍 Recomendación: cerrar posición restante.
Esperar nueva acumulación para reinicio de ciclo.
"""

    send(msg)
