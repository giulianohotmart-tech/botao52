from market_data import get_candles
import config

def trend_signal():

    df5 = get_candles(config.SYMBOL,"5m")
    df15 = get_candles(config.SYMBOL,"15m")
    df1h = get_candles(config.SYMBOL,"1h")

    ma5 = df5["close"].rolling(9).mean().iloc[-1]
    ma5_long = df5["close"].rolling(21).mean().iloc[-1]

    ma15 = df15["close"].rolling(9).mean().iloc[-1]
    ma15_long = df15["close"].rolling(21).mean().iloc[-1]

    ma1h = df1h["close"].rolling(9).mean().iloc[-1]
    ma1h_long = df1h["close"].rolling(21).mean().iloc[-1]

    if ma5 > ma5_long and ma15 > ma15_long and ma1h > ma1h_long:
        return "BUY"

    if ma5 < ma5_long and ma15 < ma15_long:
        return "SELL"

    return None