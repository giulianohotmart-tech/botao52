import matplotlib
matplotlib.use("Agg")

from flask import Flask, render_template_string
import json
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

HTML = """

<h1>BOTÃO52 Dashboard</h1>

<p><b>Preço BTC:</b> {{price}}</p>
<p><b>Saldo USDT:</b> {{balance}}</p>
<p><b>Em posição:</b> {{position}}</p>

<h2>Lucro do Bot</h2>
<p>{{profit}}</p>

<h2>Estatísticas</h2>
<p>Total de Trades: {{trades}}</p>
<p>Win Rate: {{winrate}} %</p>

<h2>Gráfico de preço</h2>
<img src="/static/chart.png" width="600">

"""


def update_chart(price):

    try:
        df = pd.read_csv("price_history.csv")
    except:
        df = pd.DataFrame(columns=["price"])

    df.loc[len(df)] = price

    if len(df) > 100:
        df = df.tail(100)

    df.to_csv("price_history.csv", index=False)

    plt.figure()
    plt.plot(df["price"])
    plt.title("BTC Price")
    plt.savefig("static/chart.png")
    plt.close()


def calculate_profit():

    try:

        df = pd.read_csv("trades.csv")

        buys = df[df["action"] == "BUY"]
        sells = df[df["action"] == "SELL"]

        profit = sells["price"].sum() - buys["price"].sum()

        return round(profit, 2)

    except:

        return 0


def trade_stats():

    try:

        df = pd.read_csv("trades.csv")

        buys = len(df[df["action"] == "BUY"])
        sells = len(df[df["action"] == "SELL"])

        trades = sells

        winrate = 0

        if trades > 0:
            winrate = round((sells / trades) * 100, 2)

        return trades, winrate

    except:

        return 0, 0


@app.route("/")
def home():

    trades, winrate = trade_stats()
    profit = calculate_profit()

    try:

        with open("status.json") as f:
            data = json.load(f)

        update_chart(data["price"])

    except:

        data = {
            "price": "-",
            "balance": "-",
            "position": "-"
        }

    return render_template_string(
        HTML,
        price=data["price"],
        balance=data["balance"],
        position=data["position"],
        profit=profit,
        trades=trades,
        winrate=winrate
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)