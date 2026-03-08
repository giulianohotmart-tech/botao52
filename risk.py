def calculate_position(balance, risk, price):

    capital_risk = balance * risk

    quantity = capital_risk / price

    return round(quantity, 6)