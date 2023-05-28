from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
import random
import os
import re

spams = []
chat_id = ""

chats_spam = []
chats_spam_text = ""
async def main():
    os.system('cls||clear')
    action = int(input("1 > добавить аккаунт\n"
                       "2 > запустить спам со всех аккаунтов\n"
                       "3 > запустить спам по чатам\n"
                       "Выберите действие > "))
    if action == 1:
        await add_account()
    elif action == 2:
        await get_sessions()
    elif action == 3:
        await get_sessions_chats()
    else:
        print("Ошибка!")
        await main()

async def add_account():
    os.system('cls||clear')
    print("Добавление аккаунта")
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
    name = "sessions/" + input("Введите название сессии >")
    app_id = 19906117
    app_hash = '7664cab4e2de780e010037028755e984'
    phone = input("Введите номер телефона > ")
    app = Client(name, app_id, app_hash, phone_number=phone, app_version="7.7.2", device_model="Lenovo Z6 Lite", system_version="11 R")
    async with app:
        await app.get_me()
    input("Аккаунт успешно добавлен! Нажмите Enter чтобы вернутся в главное меню")
    await main()

async def get_sessions():
    sessions = []
    for file in os.listdir('sessions'):
        if re.search(".session$", file):
            sessions.append(file.replace(".session", ""))
    if sessions == []:
        input("Сессий не найдено! Нажмите Enter")
        await main()
    else:
        print("Начинаем запускать аккаунты!")
        loop = asyncio.get_event_loop()
        for s in sessions:
            print("Аккаунт - "+s)
            app = Client("sessions/" + s, app_version="7.7.2", device_model="Lenovo Z6 Lite", system_version="11 R")
            loop.create_task(start_spam(app, s))

async def start_spam(app, name):
    try:
        await spamer(app, name)
    except Exception as e:
        print(f"Вылет с аккаунта {name}:\n{e}")

async def select_text(app):
    async for message in app.get_chat_history(chat_id, limit=1, offset_id=-1):
        await asyncio.sleep(1)
        return message.text
async def spamer(app, name):
    print(f"Аккаунт {name} запущен!\n\n")
    async with app:
        await app.send_message(chat_id, "/next")
    same_text_count = 0
    while True:
        async with app:
            while True:
                try:
                    if "найден" in await select_text(app):
                        await app.send_message(chat_id, random.choice(spams))
                        await asyncio.sleep(6)
                        await app.send_message(chat_id, "/next")

                        same_text_count = 0
                    else:
                        same_text_count += 1
                        if same_text_count >= 15:
                            await app.send_message(chat_id, "/stop")
                            await app.send_message(chat_id, "/stop")
                            await asyncio.sleep(2)
                            await app.send_message(chat_id, "/next")
                            same_text_count = 0

                except Exception as e:
                    if isinstance(e, FloodWait):
                        print(f"На аккаунте {name} словлен FLOOW_WAIT бан на {e.value} секунд!")
                        await asyncio.sleep(e.value)

async def get_sessions_chats():
    sessions = []
    for file in os.listdir('sessions'):
        if re.search(".session$", file):
            sessions.append(file.replace(".session", ""))
    if sessions == []:
        input("Сессий не найдено! Нажмите Enter")
        await main()
    else:
        print("Начинаем запускать аккаунты!")
        loop = asyncio.get_event_loop()
        for s in sessions:
            print("Аккаунт - "+s)
            app = Client("sessions/" + s, app_version="7.7.2", device_model="Lenovo Z6 Lite", system_version="11 R")
            loop.create_task(start_spam_chats(app, s))
async def start_spam_chats(app, name):
    try:
        await spamer_chats(app, name)
    except Exception as e:
        print(f"Вылет с аккаунта {name}:\n{e}")

async def spamer_chats(app, name):
    print(f"Аккаунт {name} запущен!\n\n")
    while True:
        async with app:
            while True:
                for i in chats_spam:
                    try:
                        await app.send_message(i, chats_spam_text)
                        await asyncio.sleep(5)
                    except:
                        pass
                await asyncio.sleep(300)

loop = asyncio.new_event_loop()
loop.create_task(main())
loop.run_forever()
input("Работа скрипта завершена, скорее всего все аккаунты отлетели")