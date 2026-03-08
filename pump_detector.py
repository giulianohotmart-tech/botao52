from market_data import get_candles
import config

def detect_pump():

    df = get_candles(config.SYMBOL,"5m",10)

    change = (df["close"].iloc[-1] - df["close"].iloc[-5]) / df["close"].iloc[-5]

    if change > 0.03:
        return "PUMP"

    if change < -0.03:
        return "DUMP"

    return None