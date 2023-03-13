#!/usr/bin/python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from enum import Enum
import json
import os
import platform
import requests
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


if __name__ == '__main__':
    send_telegram("hello world!")