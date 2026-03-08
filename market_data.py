import requests
import pandas as pd


def get_candles(symbol, interval="5m", limit=100):

    try:

        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"

        response = requests.get(url, timeout=10)

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            return pd.DataFrame({"close":[65000]})

        df = pd.DataFrame(data)

        df = df[[0,1,2,3,4]]

        df.columns = ["time","open","high","low","close"]

        df["close"] = df["close"].astype(float)

        return df

    except Exception as e:

        print("Erro ao obter candles:", e)

        return pd.DataFrame({"close":[65000]})