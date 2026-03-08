import requests
import pandas as pd


def get_candles(symbol, interval="5m", limit=100):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

    data = requests.get(url).json()

    if not isinstance(data, list):
        return pd.DataFrame(columns=["close"])

    df = pd.DataFrame(data)

    df = df[[0,1,2,3,4]]

    df.columns = ["time","open","high","low","close"]

    df["close"] = df["close"].astype(float)

    return df