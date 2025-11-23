def puntaje_holdeo(df, symbol):
    # 🔰 Validación estricta
    if df is None or not hasattr(df, "empty") or df.empty:
        print(f"[ERROR] DF vacío para {symbol}")
        return 0, ["❌ Datos insuficientes"]

    if "close" not in df.columns or len(df["close"]) < 2:
        print(f"[ERROR] Columna 'close' no válida en {symbol}")
        return 0, ["❌ Sin velas suficientes"]

    score = 0
    razones = []

    # === Datos seguros ===
    precio = df["close"].iloc[-1]

    try:
        e200 = ema200(df).iloc[-1]
    except Exception:
        e200 = precio

    try:
        rsi_v = rsi(df).iloc[-1]
    except Exception:
        rsi_v = 50
