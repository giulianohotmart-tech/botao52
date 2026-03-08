def buy(client, symbol, quantity):

    order = client.order_market_buy(
        symbol=symbol,
        quantity=quantity
    )

    print("COMPRA EXECUTADA")

    return order


def sell(client, symbol, quantity):

    order = client.order_market_sell(
        symbol=symbol,
        quantity=quantity
    )

    print("VENDA EXECUTADA")

    return order