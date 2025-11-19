import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def normalize(series):
    scaler = MinMaxScaler()
    norm = scaler.fit_transform(series.values.reshape(-1, 1))
    return norm, scaler

def arima_predict(df, steps=1):
    try:
        model = ARIMA(df["close"], order=(2, 1, 2))
        fit = model.fit()
        pred = fit.forecast(steps=steps)
        return pred[-1]
    except:
        return None

def build_lstm():
    model = Sequential()
    model.add(LSTM(32, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(16))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    return model

def lstm_predict(df, window=30):
    try:
        close = df["close"]
        norm, scaler = normalize(close)

        X, y = [], []
        for i in range(window, len(norm)):
            X.append(norm[i-window:i])
            y.append(norm[i])

        X = np.array(X).reshape(-1, window, 1)
        y = np.array(y)

        model = build_lstm()
        model.fit(X, y, epochs=5, batch_size=8, verbose=0)

        last = norm[-window:].reshape(1, window, 1)
        pred = model.predict(last)[0][0]
        return scaler.inverse_transform([[pred]])[0][0]
    except:
        return None

def pattern_probability(df, lookback=100):
    try:
        close = df["close"]
        ret = close.pct_change().dropna()
        last = ret.iloc[-20:].mean()

        similar = ret.rolling(20).mean()
        diff = (similar - last).abs()
        matches = diff[diff < 0.001]

        if len(matches) == 0:
            return 0.5

        prob = len(matches) / lookback
        return min(max(prob, 0.05), 0.95)
    except:
        return 0.5

def ai_score(df):
    try:
        close = df["close"].iloc[-1]

        a1 = arima_predict(df, 1)
        a4 = arima_predict(df, 4)
        a24 = arima_predict(df, 24)

        lstm = lstm_predict(df)
        pat = pattern_probability(df)

        score = 0

        for p in [a1, a4, a24]:
            if p is not None:
                score += 0.13 if p > close else -0.13

        if lstm:
            score += 0.4 if lstm > close else -0.4

        score += (pat - 0.5) * 0.4

        prob = (score + 1) / 2
        prob = round(prob * 100, 2)

        return {
            "arima_1h": a1,
            "arima_4h": a4,
            "arima_24h": a24,
            "lstm": lstm,
            "pattern_prob": pat,
            "confidence": prob
        }

    except:
        return {
            "arima_1h": None,
            "arima_4h": None,
            "arima_24h": None,
            "lstm": None,
            "pattern_prob": 0.5,
            "confidence": 50
      }
