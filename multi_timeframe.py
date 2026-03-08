from market_data import get_candles
import config


def trend_signal():

    try:

        df = get_candles(config.SYMBOL)

        if len(df) < 20:
            return None

        ma9 = df["close"].rolling(9).mean().iloc[-1]
        ma21 = df["close"].rolling(21).mean().iloc[-1]

        if ma9 > ma21:
            return "BUY"

        if ma9 < ma21:
            return "SELL"

        return None

    except Exception as e:

        print("Erro trend:", e)

        return None