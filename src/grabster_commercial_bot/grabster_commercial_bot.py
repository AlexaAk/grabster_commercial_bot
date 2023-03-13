#!/usr/bin/python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from enum import Enum
import json
import os
import platform
import schedule
import time
import requests
import threading
if platform.system() == "Linux":
    os.chdir("/home/alexaak/python/Buh_bots/")
else:
    os.chdir("../../")
import keyboards as kb
import creating as cr
import posting as pst

jsonConfig = open("config.json", "r", encoding="utf-8")
json_file = json.load(jsonConfig)

bot = Bot(token=json_file["token_bot"])
jsonConfig.close()

dp = Dispatcher(bot)
users = {}


class Stage(Enum):
    NONE = 0


def send_telegram(text: str):
    token = "6117678229:AAG7yE3vseScGXU6YuaLgYCZXybvkhaWCVw"
    url = "https://api.telegram.org/bot"
    channel_id = "@grabster_radio"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")


def job():
    send_telegram("сейчас 18:59")


def thread_function():
    schedule.every().day.at("18:59").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    x = threading.Thread(target=thread_function)
    send_telegram("hello world!")