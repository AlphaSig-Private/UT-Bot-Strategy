from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Emoji mappings
ASSET_EMOJIS = {
    "SOL": "💥",
    "PEPE": "🐸"
}

DIRECTION_EMOJIS = {
    "BUY": "🟢 BUY signal 🚀",
    "SELL": "🔴 SELL / SHORT 💀"
}

TIMEFRAME_LABELS = {
    "1D": "DAILY",
    "1W": "WEEKLY",
    "1M": "MONTHLY"
}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    pair = data.get("pair", "UNKNOWN/USDT")
    symbol = data.get("symbol", "UNKNOWN").upper()
    direction = data.get("direction", "BUY").upper()
    timeframe = data.get("timeframe", "1D").upper()

    asset_emoji = ASSET_EMOJIS.get(symbol, "")
    direction_text = DIRECTION_EMOJIS.get(direction, "")
    timeframe_text = TIMEFRAME_LABELS.get(timeframe, timeframe)

    message = f"{asset_emoji} {pair} 💵 – {direction_text} on the {timeframe_text} Chart"

    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    requests.post(telegram_url, json={"chat_id": chat_id, "text": message})
    return "Alert sent", 200

