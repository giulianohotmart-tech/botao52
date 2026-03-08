import csv
from datetime import datetime

def log_trade(action, price, quantity):

    with open("trades.csv", "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now(),
            action,
            price,
            quantity
        ])