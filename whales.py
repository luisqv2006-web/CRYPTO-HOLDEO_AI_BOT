import requests

EXCHANGES = [
    "binance", "coinbase", "kraken", "bitfinex",
    "kucoin", "huobi", "okx", "bybit"
]

def fetch_whale_data(min_usd=5000000):
    try:
        url = "https://api.whale-alert.io/v1/transactions?limit=50"
        data = requests.get(url, timeout=5).json()

        if "transactions" not in data:
            return []

        events = []

        for tx in data["transactions"]:
            usd = tx.get("amount_usd", 0)
            if usd < min_usd:
                continue

            src = tx.get("from", {}).get("owner", "unknown").lower()
            dst = tx.get("to", {}).get("owner", "unknown").lower()

            asset = tx.get("symbol", "").upper()

            events.append({
                "asset": asset,
                "amount_usd": usd,
                "source": src,
                "dest": dst
            })

        return events

    except:
        return []

def classify_whale_event(e):
    usd = e["amount_usd"]
    coin = e["asset"]
    src = e["source"]
    dst = e["dest"]

    if any(ex in dst for ex in EXCHANGES):
        return f"🔴 Venta posible — {coin}\n🐳 Ballena envió ${usd:,.0f} a un exchange."

    if any(ex in src for ex in EXCHANGES):
        return f"🟢 Acumulación — {coin}\n💼 Retiro institucional de ${usd:,.0f}."

    return f"⚪ Movimiento grande — {coin}\n${usd:,.0f} entre wallets privadas."

def whale_monitor(min_usd=5000000):
    events = fetch_whale_data(min_usd)
    alerts = []

    for e in events:
        alerts.append(classify_whale_event(e))

    return alerts[:5]
