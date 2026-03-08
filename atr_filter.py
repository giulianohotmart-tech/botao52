import pandas as pd
from market_data import get_candles
import config
from ta.volatility import AverageTrueRange


def atr_signal():

    df = get_candles(config.SYMBOL, "5m", 100)

    atr = AverageTrueRange(
        high=df["close"],
        low=df["close"],
        close=df["close"],
        window=14
    )

    df["atr"] = atr.average_true_range()

    last_atr = df["atr"].iloc[-1]

    if last_atr > df["atr"].mean():
        return True

    return False