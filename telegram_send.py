import telegram
from dotenv import load_dotenv
import os
import asyncio
import time

# Load the environment variables
load_dotenv()

# Get the API key from the environment variables
# We pushed the key because it doesn't work anymore and we didnt have keyboard in raspi
telegram_api_key = os.getenv("TELEGRAM_API_KEY")

bot = telegram.Bot(token=telegram_api_key)


class TelegramBot:
    def __init__(self):
        self.bot = telegram.Bot(token=telegram_api_key)

    async def trigger_send_message(heartbeats: int):
        # Get the number of heartbeats
        # Get actual unix time
        unix_time = int(time.time())
        # Transform unix time to human readable time
        measure_time = time.strftime("%H:%M:%S %d-%m-%Y")

        if heartbeats < 60:
            texto = f"Peligro: Ritmo cardiaco bajo {heartbeats} BPS. Medido a las {measure_time}"
        elif heartbeats > 100:
            texto = f"Peligro: Ritmo cardiaco alto {heartbeats} BPS. Medido a las {measure_time}"
        else:
            texto = f"Ritmo cardiaco normal {heartbeats} BPS. Medido a las {measure_time}"

        async with bot:
            await bot.send_message(chat_id="-4258733131", text=texto)

