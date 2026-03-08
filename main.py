import json
import time
import requests

import config

from multi_timeframe import trend_signal
from pump_detector import detect_pump
from market_filter import market_volatility, market_sideways
from atr_filter import atr_signal

from strategy import check_signal
from trade import buy, sell
from risk import calculate_position
from logger import log_trade
from dashboard import show


# criar client da Binance apenas se não for paper trading
if config.PAPER_TRADING:
    client = None
else:
    from binance.client import Client
    client = Client(config.API_KEY, config.API_SECRET)


prices = []
position = False
entry_price = 0
quantity = 0


def get_price():

    # pegar preço via API pública (não bloqueada)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={config.SYMBOL}"
    data = requests.get(url).json()

    return float(data["price"])


def get_balance():

    # saldo simulado para paper trading
    if config.PAPER_TRADING:
        return 1000

    balance = client.get_asset_balance(asset="USDT")
    return float(balance["free"])


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

            # mostrar status no terminal
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

            # tendência multi timeframe
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

                if config.PAPER_TRADING:
                    print("SIMULAÇÃO COMPRA:", quantity)
                else:
                    buy(client, config.SYMBOL, quantity)

                entry_price = price
                position = True

                log_trade("BUY", price, quantity)

            elif position:

                profit = (price - entry_price) / entry_price

                if profit <= -config.STOP_LOSS:

                    if config.PAPER_TRADING:
                        print("SIMULAÇÃO STOP LOSS")
                    else:
                        sell(client, config.SYMBOL, quantity)

                    position = False
                    log_trade("STOP", price, quantity)

                elif profit >= config.TAKE_PROFIT:

                    if config.PAPER_TRADING:
                        print("SIMULAÇÃO TAKE PROFIT")
                    else:
                        sell(client, config.SYMBOL, quantity)

                    position = False
                    log_trade("TAKE PROFIT", price, quantity)

        except Exception as e:

            print("Erro:", e)

        time.sleep(config.INTERVAL)


if __name__ == "__main__":

    run_bot()