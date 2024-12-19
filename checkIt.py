import requests
import pandas as pd

def get_rsi():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 14
    }
    response = requests.get(url, params=params)
    data = response.json()
    close_prices = [float(candle[4]) for candle in data]
    df = pd.DataFrame(close_prices, columns=["close"])
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

print(get_rsi())