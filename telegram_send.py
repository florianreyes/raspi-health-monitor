import telegram
from dotenv import load_dotenv
import os
import asyncio
import time
from database import insert_medicion

CLIENTE = "gonzo-floro"

# Load the environment variables
load_dotenv()

# Get the API key from the environment variables
telegram_api_key = os.getenv("TELEGRAM_API_KEY")

bot = telegram.Bot(token=telegram_api_key)


async def send_message():
    # Get the number of heartbeats
    heartbeats = get_heartbeats()

    # Get actual unix time
    unix_time = int(time.time())
    # Transform unix time to human readable time
    measure_time = time.strftime("%H:%M:%S %d-%m-%Y")

    # Insert the measurement into the database
    insert_medicion(unix_time, heartbeats, CLIENTE)

    if heartbeats < 60:
        texto = f"Peligro: Ritmo cardiaco bajo {heartbeats} BPS. Medido a las {measure_time}"
    elif heartbeats > 100:
        texto = f"Peligro: Ritmo cardiaco alto {heartbeats} BPS. Medido a las {measure_time}"
    else:
        texto = f"Ritmo cardiaco normal {heartbeats} BPS. Medido a las {measure_time}"

    async with bot:
        await bot.send_message(chat_id="-4258733131", text=texto)


def get_heartbeats():
    values = [40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    return values[int(time.time()) % 12]


if __name__ == "__main__":
    while True:
        asyncio.run(send_message())
        time.sleep(5)
