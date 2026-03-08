import json
import time
import requests

import config

trend_signal = lambda: None
detect_pump = lambda: None
market_volatility = lambda prices: True
market_sideways = lambda prices: False
atr_signal = lambda: True

from strategy import check_signal
from risk import calculate_position
from logger import log_trade
from dashboard import show


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

        print("Resposta inesperada da API:", data)

    except Exception as e:

        print("Erro ao obter preço:", e)

    if prices:
        return prices[-1]

    return 65000


def get_balance():

    # saldo simulado para paper trading
    if config.PAPER_TRADING:
        return 1000

    # caso futuramente rode em VPS com Binance real
    return 0


def run_bot():

    global position
    global entry_price
    global quantity

    print("BOTÃO52 iniciado")

    while True:

        try:

            price = get_price()

            prices.append(price)

            balance = get_balance()

            show(price, balance, position)

            # atualizar dashboard
            status = {
                "price": price,
                "balance": balance,
                "position": position
            }

            with open("status.json", "w") as f:
                json.dump(status, f)

            # detectar pump / dump
            pump = detect_pump()

            if pump == "PUMP":
                print("🚀 PUMP detectado")

            if pump == "DUMP":
                print("⚠️ DUMP detectado")

            # tendência
            trend = trend_signal()

            if trend:
                print("Trend:", trend)

            # filtros de mercado

            if not market_volatility(prices):

                print("Mercado sem volatilidade")

                time.sleep(config.INTERVAL)

                continue

            if market_sideways(prices):

                print("Mercado lateral")

                time.sleep(config.INTERVAL)

                continue

            if not atr_signal():

                print("Volatilidade baixa (ATR)")

                time.sleep(config.INTERVAL)

                continue

            signal = check_signal(prices)

            if signal == "BUY" and not position:

                quantity = calculate_position(
                    balance,
                    config.TRADE_PERCENTAGE,
                    price
                )

                print("SIMULAÇÃO COMPRA:", quantity)

                entry_price = price

                position = True

                log_trade("BUY", price, quantity)

            elif position:

                profit = (price - entry_price) / entry_price

                if profit <= -config.STOP_LOSS:

                    print("SIMULAÇÃO STOP LOSS")

                    position = False

                    log_trade("STOP", price, quantity)

                elif profit >= config.TAKE_PROFIT:

                    print("SIMULAÇÃO TAKE PROFIT")

                    position = False

                    log_trade("TAKE PROFIT", price, quantity)

        except Exception as e:

            print("Erro:", e)

        time.sleep(config.INTERVAL)


if __name__ == "__main__":

    run_bot()