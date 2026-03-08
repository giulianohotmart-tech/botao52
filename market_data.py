from binance.client import Client
import pandas as pd
import config

client = Client(config.API_KEY, config.API_SECRET)

def get_candles(symbol, interval, limit=100):

    candles = client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

    df = pd.DataFrame(candles)

    df = df[[0,4]]

    df.columns = ["time","close"]

    df["close"] = df["close"].astype(float)

    return df