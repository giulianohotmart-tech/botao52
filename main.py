import json
import time
import requests
import config

prices = []
position = False
entry_price = 0
quantity = 0


def get_price():

    try:

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={config.SYMBOL}"

        response = requests.get(url, timeout=10)

        data = response.json()

        if "price" in data:
            return float(data["price"])

    except Exception as e:

        print("Erro API:", e)

    if prices:
        return prices[-1]

    return 65000


def run_bot():

    global position
    global entry_price
    global quantity

    print("BOTÃO52 iniciado")

    while True:

        try:

            price = get_price()

            prices.append(price)

            balance = 1000

            print("------------------")
            print("Preço BTC:", price)
            print("Saldo USDT:", balance)
            print("Em posição:", position)
            print("------------------")

            status = {
                "price": price,
                "balance": balance,
                "position": position
            }

            with open("status.json", "w") as f:
                json.dump(status, f)

        except Exception as e:

            print("Erro:", e)

        time.sleep(config.INTERVAL)


if __name__ == "__main__":
    run_bot()