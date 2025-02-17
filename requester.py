import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher

API_TOKEN = '7573998446:AAGM1MVdlYtR8e854zqRujEHDk3GoxqHRLc'
GROUP_ID = '-1002438140253'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

tour_number = 716

sign_in_url = "https://api.zakovatklubi.uz/v1/user/sign-in?&_l=uz"
reg_url = "https://api.zakovatklubi.uz/v1/user/request?&_l=uz"
url = f"https://api.zakovatklubi.uz/v1/tournament/{tour_number}?include=clubCount,personCount,teamCount,categories,file,seasons,tours.matches,is_subscription&_l=uz"
headers = {
    "accept": "application/json",
    "authorization": "Bearer Bvy8EtiU3eBRzOuUQ_sDx4FhsyIKlZPdqHAWsJBaYF88QqXALXN4Ro5aQY8pTLpm"
}

sign_params = [{
    "phone": "+998994246558",
    "password": "Sirojiddin2004;"
},
    {
        "phone": "+998935011112",
        "password": "Shoaziz17"
    }]


def sign_in(sign_param):
    response1 = requests.get(sign_in_url, params=sign_param)
    if response1.status_code == 200:
        return response1.json()['data']['token']
    else:
        return None


reg_headers1 = {
    "accept": "application/json",
    "authorization": f"Bearer {sign_in(sign_params[0])}"
}
reg_headers2 = {
    "accept": "application/json",
    "authorization": f"Bearer {sign_in(sign_params[1])} "
}

params1 = {
    "title": '"null"',
    "description": "null",
    "logo_id": 231215,
    "club_id": 10035,
    "team_id": 28037,
    "type": 1,
    "tournament_id": tour_number,
    "mainPersonIds": [360996, 364921],
    "reservePersonIds": []
}

params2 = {
    "title": '"4ever young"',
    "description": "null",
    "logo_id": 234401,
    "club_id": 10035,
    "team_id": 27082,
    "type": 1,
    "tournament_id": tour_number,
    "mainPersonIds": [165782, 332878, 332879, 332881, 364919],
    "reservePersonIds": []
}


def fetch_data_from_api():
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and "Quiz" in response.json()['data']['title']:
        data = response.json()
        quiz_title = data['data']['title']
        text = f"""{quiz_title} quizga ro'yxatdan o'tish boshlandi
"""

        return text
    else:
        return None


def auto_register():
    response1 = requests.post(reg_url, headers=reg_headers1, params=params1)
    response2 = requests.post(reg_url, headers=reg_headers2, params=params2)
    print(response1.json())
    if response1.json()['message'] == "So'rov muvaffaqiyatli yuborildi" and response2.json()[
        'message'] == "So'rov muvaffaqiyatli yuborildi":
        return "Jamoalar muvaffaqiyatli ro'yxatdan o'tkazildi!"
    else:
        return None


async def send_data_to_group():
    # Fetch data from the API
    data = fetch_data_from_api()

    if data:
        message = await bot.send_message(GROUP_ID, data)
        await bot.pin_chat_message(GROUP_ID, message.message_id)
        reg_text = auto_register()
        await bot.send_message(GROUP_ID, reg_text)
        os.system('pkill -f requester.py')
    else:
        print("No data received from API.")


async def schedule_task():
    while True:
        await send_data_to_group()
        await asyncio.sleep(20)


async def main():
    asyncio.create_task(schedule_task())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
