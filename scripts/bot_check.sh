#!/bin/bash
ps -A | grep task_bot.py || /home/alexaak/python/Buh_bots/src/task_bot/task_bot.py >> /home/alexaak/python/Buh_bots/log.txt 2>&1 &
