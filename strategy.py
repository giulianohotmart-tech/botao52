import pandas as pd

def check_signal(prices):

    if len(prices) < 50:
        return None

    df = pd.DataFrame(prices, columns=["price"])

    df["ma9"] = df["price"].rolling(9).mean()
    df["ma21"] = df["price"].rolling(21).mean()
    df["ma50"] = df["price"].rolling(50).mean()

    last = df.iloc[-1]

    if last["ma9"] > last["ma21"] and last["ma21"] > last["ma50"]:
        return "BUY"

    if last["ma9"] < last["ma21"]:
        return "SELL"

    return None