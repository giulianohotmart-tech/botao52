import requests
import config

def send_telegram(message):

    try:

        url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"

        payload = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message
        }

        requests.post(url, data=payload)

    except Exception as e:

        print("Erro Telegram:", e)