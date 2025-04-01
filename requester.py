import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher

API_TOKEN = '7573998446:AAGM1MVdlYtR8e854zqRujEHDk3GoxqHRLc'
GROUP_ID = '-1002438140253'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

tour_number = 734

sign_in_url = "https://api.zakovatklubi.uz/v1/user/sign-in?&_l=uz"
reg_url = "https://api.zakovatklubi.uz/v1/user/request?&_l=uz"
tour_url = f"https://api.zakovatklubi.uz/v1/tournament/{tour_number}?include=clubCount,personCount,teamCount,categories,file,seasons,tours.matches,is_subscription&_l=uz"
transfers_url = "https://api.zakovatklubi.uz/v1/user/transfer-request?include=team,club,person,tournament,coordinator,oldClub&per-page=5&sort=-created_at&_l=uz"

sign_params = [
    {
        "phone": "+998994246558",
        "password": "Sirojiddin2004;"
    },
    {
        "phone": "+998500060244",
        "password": "90M2EZUV"
    },
    {
        "phone": "+998934246558",
        "password": "Sirojiddin2004;"
    }
]


def sign_in(sign_param):
    response1 = requests.get(sign_in_url, params=sign_param)
    if response1.status_code == 200:
        return response1.json()['data']['token']
    else:
        return None


reg_headers1 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {sign_in(sign_params[0])}"
}

reg_headers2 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {sign_in(sign_params[1])}"
}

reg_headers3 = {
    "Accept": "application/json",
    "Authorization": f"Bearer {sign_in(sign_params[2])}"
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

# params2 = {
#     "title": '4ever young',
#     "description": "null",
#     "logo_id": 234401,
#     "club_id": 10035,
#     "team_id": 27082,
#     "type": 1,
#     "tournament_id": tour_number,
#     "mainPersonIds": [332878, 332879, 332881, 364919, 165782],
#     "reservePersonIds": []
# }


def fetch_data_from_api():
    response = requests.get(tour_url)
    if response.status_code == 200:
        data = response.json()
        quiz_title = data['data']['title']
        text = f"""{quiz_title}ga ro'yxatdan o'tish boshlandi
url: https://zakovatklubi.uz/tournaments/{tour_number}"""
        return text
    else:
        return None


def auto_register():
    response1 = requests.post(reg_url, headers=reg_headers1, json=params1)
    # response2 = requests.post(reg_url, headers=reg_headers4, json=params2)
    if response1.json()['message'] == "So'rov muvaffaqiyatli yuborildi":
        return "null muvaffaqiyatli ro'yxatdan o'tkazildi!"
    else:
        return None


def accept_transfer():
    id_response = requests.get(transfers_url, headers=reg_headers2)
    id_response1 = requests.get(transfers_url, headers=reg_headers3)
    if id_response.json()['data'][0]['tournament_id'] == tour_number:
        transfer_id1 = id_response.json()['data'][0]['id']
        transfer_id2 = id_response1.json()['data'][0]['id']
        transfer_accept_url1 = f"https://api.zakovatklubi.uz/v1/user/accept-transfer-request/{transfer_id1}?&_l=uz"
        transfer_accept_url2 = f"https://api.zakovatklubi.uz/v1/user/accept-transfer-request/{transfer_id2}?&_l=uz"
        response = requests.post(transfer_accept_url1, headers=reg_headers2)
        response1 = requests.post(transfer_accept_url2, headers=reg_headers3)
        if response.json()['code'] == 1 and response1.json()['code'] == 1:
            return "null a'zolarining transferlari qabul qilindi!"
        else:
            return None


async def send_data_to_group():
    data = fetch_data_from_api()
    if data:
        await bot.send_message(GROUP_ID, data)
        if "Quiz" in data:
            reg_text = auto_register()
            await bot.send_message(GROUP_ID, reg_text)
            accept_text = accept_transfer()
            await bot.send_message(GROUP_ID, accept_text)
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
