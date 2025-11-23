def analizar_symbol(symbol):
    df = get_klines(symbol, "1d", 200)

    # Validación global
    if df is None or not hasattr(df, "empty") or df.empty:
        print(f"[SKIP] Sin datos para {symbol}")
        return

    # Validar columnas mínimas
    if "close" not in df.columns:
        print(f"[SKIP] Sin columna 'close' para {symbol}")
        return

    # Validar cantidad mínima de velas
    if len(df) < 50:
        print(f"[SKIP] {symbol} tiene solo {len(df)} velas, insuficiente")
        return

    # Calcular señal
    score, razones = puntaje_holdeo(df, symbol)
    if score < UMBRAL_SENAL:
        return

    # Cálculo de entrada
    try:
        precio = df["close"].iloc[-1]
    except Exception:
        print(f"[ERROR] No se pudo obtener precio de cierre en {symbol}")
        return

    stop_pct = 0.09

    monto_info = calcular_monto(precio, stop_pct)
    tp1, tp2, tp3 = calcular_tps(precio, stop_pct)

    enviar_alerta(symbol, score, razones, monto_info, tp1, tp2, tp3)
