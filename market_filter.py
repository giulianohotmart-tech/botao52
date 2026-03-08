import pandas as pd

def market_volatility(prices):

    if len(prices) < 20:
        return False

    df = pd.DataFrame(prices, columns=["price"])

    df["returns"] = df["price"].pct_change()

    volatility = df["returns"].std()

    if volatility > 0.002:
        return True

    return False


def market_sideways(prices):

    if len(prices) < 30:
        return False

    df = pd.DataFrame(prices, columns=["price"])

    df["ma20"] = df["price"].rolling(20).mean()

    last_price = df.iloc[-1]["price"]
    ma = df.iloc[-1]["ma20"]

    distance = abs(last_price - ma) / ma

    if distance < 0.0015:
        return True

    return False