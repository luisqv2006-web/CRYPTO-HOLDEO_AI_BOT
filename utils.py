import requests
import pandas as pd

def get_klines(symbol="BTCUSDT", interval="1h", limit=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        data = requests.get(url, params=params, timeout=5).json()
        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote", "trades", "tbb", "tbq", "ignore"
        ])
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df[["open", "high", "low", "close", "volume"]]
    except:
        return None

def log(msg):
    print(f"[LOG] {msg}")
