from market_data import get_candles
import pandas as pd


def run_backtest():

    print("Iniciando backtest...")

    df = get_candles("BTCUSDT", "5m", 500)

    df["ma9"] = df["close"].rolling(9).mean()
    df["ma21"] = df["close"].rolling(21).mean()

    balance = 1000
    position = False
    entry = 0
    trades = 0

    for i in range(len(df)):

        row = df.iloc[i]

        if pd.isna(row["ma9"]) or pd.isna(row["ma21"]):
            continue

        # compra
        if row["ma9"] > row["ma21"] and not position:

            entry = row["close"]
            position = True
            trades += 1

        # venda
        elif row["ma9"] < row["ma21"] and position:

            profit = row["close"] - entry
            balance += profit
            position = False

    print("----------------------------")
    print("Backtest finalizado")
    print("Trades executados:", trades)
    print("Saldo inicial: 1000")
    print("Saldo final:", round(balance, 2))
    print("Lucro:", round(balance - 1000, 2))
    print("----------------------------")


if __name__ == "__main__":

    run_backtest()