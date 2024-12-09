import asyncio
import logging
import os
from os import system

import requests
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from datetime import datetime, timezone

API_TOKEN = '7573998446:AAGM1MVdlYtR8e854zqRujEHDk3GoxqHRLc'
GROUP_ID = '-4569840993'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

url = "https://api.zakovatklubi.uz/v1/tournament/682?include=clubCount,personCount,teamCount,categories,file,seasons,tours.matches,is_subscription&_l=uz"
headers = {
    "accept": "application/json",
    "authorization": "Bearer wz6EkzsFVyqrE7Ef14Mtf6Mg3C2_WYaq7ysbsPpj1yTFtUuTt51C57Et4PpGjf_t"
}


def fetch_data_from_api():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        quiz_title = data['data']['title']
        start_date = data['data']['start_at']
        team_count = data['data']['teamCount']
        person_count = data['data']['personCount']
        accept_request = data['data']['accept_request']

        readable_start_date = datetime.fromtimestamp(start_date, timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        accept_request = "ochiq" if accept_request else "yopildi"

        text = f"""{quiz_title} quizga ro'yxatdan o'tish boshlandi
Start Date: {readable_start_date}
{team_count}ta jamoa ro'yxatdan o'tdi
{person_count} ta odam ro'yxatdan o'tib bo'ldi
Ro'yxatdan o'tish: {accept_request}
"""

        return text
    else:
        return None


# Function to send the data to the group and pin it
async def send_data_to_group():
    # Fetch data from the API
    data = fetch_data_from_api()

    if data:
        message = await bot.send_message(GROUP_ID, data, parse_mode=ParseMode.MARKDOWN)
        await bot.pin_chat_message(GROUP_ID, message.message_id)
        os.system('systemctl stop scheduler.service')
    else:
        print("No data received from API.")


async def schedule_task():
    while True:
        await send_data_to_group()
        await asyncio.sleep(60)


async def main():
    asyncio.create_task(schedule_task())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
