import requests

from config.settings import TELEGRAM_BOT_TOKEN


def send_message(message, chat_id) -> None:
    """Отправка сообщения в 'Телеграмм'"""
    params = {"text": message, "chat_id": chat_id}
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
