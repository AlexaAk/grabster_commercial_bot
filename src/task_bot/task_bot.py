#!/usr/bin/python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from enum import Enum
import json
import os
import platform
if platform.system() == "Linux":
    os.chdir("/home/alexaak/python/Buh_bots/")
else:
    os.chdir("../../")
import keyboards as kb
import buh
import datetime


# process stages ------------------------------------------------------------------------------------------------------
class Stage(Enum):
    NONE = 0
    EMPLOYEE_NAME = 1
    TASK_NUM = 2
    PRICE = 3
    TASK_NAME = 4
    ALREADY_EXISTS = 5
    IF_EXISTS = 6
    PROJECT_NAME = 7
    # IS_PAID = 6
    TASK_LINK = 8
    PROJECT_LINK = 9
    NEW_EMPLOYEE_NAME = 10
    NEW_EMPLOYEE_BANK = 11
    GET_NEW_EMPL_INFO = 12
    GETTING_MESSAGE = 13
    EMPLOYEE_EDIT = 14
    EDIT_NAME = 15
    EDIT_BANK = 16
    EDIT_TG = 17


# bot creation --------------------------------------------------------------------------------------------------------
json_config = open("config.json", "r", encoding="utf-8")
json_file = json.load(json_config)

bot = Bot(token=json_file["token_task_bot"])
json_config.close()

dp = Dispatcher(bot)

# user stuff ----------------------------------------------------------------------------------------------------------
users = {}


class User:
    def __init__(self):
        # self.user_id = id
        self.task = buh.Task()
        self.stage = Stage.NONE
        self.tasks_in_total = 0
        self.qur_task = 0
        self.new_us_name = ''
        self.get_info_message = ''
        self.edit_us_num = 0

    def clear_user (self):
        self.task = self.task = buh.Task()
        self.stage = Stage.NONE
        self.tasks_in_total = 0
        self.qur_task = 0
        self.new_us_name = ''
        self.get_info_message = ''


def create_user_session(user_id):
    users[user_id] = User()
    users[user_id].Task = buh.Task()
    users[user_id].stage = Stage.NONE


# main menu -----------------------------------------------------------------------------------------------------------
async def main_menu (message):
    user_id = message.chat.id
    create_user_session(user_id)
    await bot.send_message(user_id,
                           "Здравствуйте! Чем займемся сегодня? 🌿", reply_markup=kb.inline_kb_main)
    users[user_id].stage = Stage.NONE


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.chat.id
    create_user_session(user_id)
    await main_menu(message)


# the great message handler -------------------------------------------------------------------------------------------
@dp.message_handler()
async def stuff_by_letter(message: types.Message):
    # creating user session if no /start command was used
    user_id = message.chat.id
    if len(users) == 0:
        create_user_session(user_id)

    # getting message text
    m_t = message.text

    # doing stuff depending on stage
    if users[user_id].stage == Stage.NONE:  # -------------------------------------------------------- NONE -----------
        await main_menu(message)

    # --------------------------------------------------------------- EMPLOYEE_NAME -- and -- EMPLOYEE_EDIT -----------
    elif users[user_id].stage == Stage.EMPLOYEE_NAME or users[user_id].stage == Stage.EMPLOYEE_EDIT:
        if len(message.text) != 1:
            if users[user_id].stage == Stage.EMPLOYEE_NAME:
                await bot.send_message(user_id, 'Введите первую букву фамилии сотрудника, которому необходимо '
                                            'отправить оплату')
            else:
                await bot.send_message(user_id, 'Введите первую букву фамилии сотрудника')
            return
        char = m_t
        list_c = []
        list_1 = []
        list_2 = []
        list_c.append(list_1)
        list_c.append(list_2)
        json_config_1 = open("config.json", "r", encoding="utf-8")
        json_file_1 = json.load(json_config_1)
        employee = json_file_1["list_employee_names"]
        json_config_1.close()
        for i in range(len(employee)):
            if len(employee[i]) != 0:
                if employee[i][0] == char.upper():
                    list_c[0].append(employee[i])
                    list_c[1].append(i)
        if len(list_c[0]) == 0:
            await bot.send_message(user_id, 'Таких сотрудников нет')
        else:
            kb.clean_stuff_kb()
            kb.fill_stuff_kb(list_c)
            await bot.send_message(user_id, 'Выберите сотрудника: ', reply_markup=kb.stuff_kb_list[0])

    elif users[user_id].stage == Stage.TASK_NUM:  # ---------------------------------------------- TASK_NUM -----------
        if m_t.isdigit():
            users[user_id].Task.set_task_num(int(m_t))
            users[user_id].tasks_in_total = m_t
            users[user_id].qur_task = 1
            users[user_id].stage = Stage.PRICE
            await bot.send_message(user_id, 'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id, 'Некорректный ввод!\n\nВведите количество задач для данного '
                                            'сотрудника')

    elif users[user_id].stage == Stage.PRICE:  # ---------------------------------------------------- PRICE -----------
        if m_t.isdigit():
            users[user_id].Task.set_price(int(m_t))
            users[user_id].stage = Stage.TASK_NAME
            await bot.send_message(user_id, 'Введите название задачи ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id,
                                   'Некорректный ввод!\n\nВведите сумму оплаты для задачи' + str(
                                       users[user_id].qur_task))

    elif users[user_id].stage == Stage.TASK_NAME:  # -------------------------------------------- TASK_NAME -----------
        users[user_id].Task.set_task_name(m_t)
        users[user_id].stage = Stage.ALREADY_EXISTS
        await bot.send_message(user_id, 'Перевод по данной задаче:', reply_markup=kb.inline_kb_exists)

    elif users[user_id].stage == Stage.ALREADY_EXISTS:  # ---------------------------------- ALREADY_EXISTS -----------
        await bot.send_message(user_id, 'Перевод по данной задаче:', reply_markup=kb.inline_kb_exists)

    elif users[user_id].stage == Stage.IF_EXISTS:  # -------------------------------------------- IF_EXISTS -----------
        if m_t.isdigit():
            users[user_id].Task.set_if_exists_price(int(m_t))
            users[user_id].stage = Stage.PROJECT_NAME
            await bot.send_message(user_id, 'Введите название проекта ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id, 'Вы ввели не число!\nВведите полную сумму будущей оплаты: ')

    elif users[user_id].stage == Stage.PROJECT_NAME:  # -------------------------------------- PROJECT_NAME -----------
        users[user_id].Task.set_project_name(m_t)
        users[user_id].stage = Stage.TASK_LINK
        await bot.send_message(user_id, 'Введите ссылку на задачу. Если у вас нет ссылки, '
                                        'нажмите на кнопку', reply_markup=kb.inline_kb_links2)

    elif users[user_id].stage == Stage.TASK_LINK:  # -------------------------------------------- TASK_LINK -----------
        users[user_id].Task.set_task_link(m_t)
        users[user_id].stage = Stage.PROJECT_LINK
        await bot.send_message(user_id, 'Введите ссылку на проект. Если у вас нет ссылки, '
                                        'нажмите на кнопку', reply_markup=kb.inline_kb_links1)

    elif users[user_id].stage == Stage.PROJECT_LINK:  # -------------------------------------- PROJECT_LINK -----------
        users[user_id].Task.set_project_link(m_t)
        if int(users[user_id].qur_task) == int(users[user_id].tasks_in_total):
            await bot.send_message(user_id, 'Все поля заполнены, высылаю готовое сообщение...')
            await bot.send_message(user_id, users[user_id].Task.compose_a_message(), reply_markup=kb.inline_kb_send_msg)
            users[user_id].stage = Stage.NONE
        else:
            users[user_id].stage = Stage.PRICE
            users[user_id].qur_task += 1
            await bot.send_message(user_id, 'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))

    elif users[user_id].stage == Stage.NEW_EMPLOYEE_NAME:  # ---------------------------- NEW_EMPLOYEE_NAME -----------
        m_t = m_t[0].upper() + m_t[1:]
        users[user_id].new_us_name = m_t
        users[user_id].stage = Stage.NEW_EMPLOYEE_BANK
        await bot.send_message(user_id,
                               'Укажите банк для данного сотрудника. Если нужного банка или электронного кошелька нет '
                               'в списка - выберите вариант Другой.', reply_markup=kb.inline_kb_banks)

    elif users[user_id].stage == Stage.NEW_EMPLOYEE_BANK:  # ---------------------------- NEW_EMPLOYEE_BANK -----------
        await bot.send_message(user_id,
                               'Укажите банк для данного сотрудника. Если у него электронный кошелек, или банк не из'
                               ' списка - нажмите кнопку Другой', reply_markup=kb.inline_kb_banks)

    elif users[user_id].stage == Stage.GET_NEW_EMPL_INFO:  # ---------------------------- GET_NEW_EMPL_INFO -----------
        m_t = '@alexa_ak, \n' + m_t
        users[user_id].get_info_message = m_t
        await bot.send_message(user_id,
                               'Вот такой вот запрос получился: \n' + m_t, reply_markup=kb.inline_kb_send_msg)

    elif users[user_id].stage == Stage.GETTING_MESSAGE:  # -------------------------------- GETTING_MESSAGE -----------
        if m_t[0] == '{':
            json_string = json.loads(message.text)
            # print(message.date)  # Вывод даты типо 20:58:30 05.07.2020
            time = message.date.time()
            s = ''
            if time < datetime.time(12):
                s += 'Доброе утро,\n'
            elif time < datetime.time(17):
                s += 'Добрый день,\n'
            elif time < datetime.time(23):
                s += 'Добрый вечер,\n'
            else:
                s += 'Доброй ночи,\n'
            s += 'Перевела '
            s += str(json_string["total_price"])
            s += ' на '
            if json_string["employee_bank"] != "":
                s += json_string["employee_bank"]
            else:
                s += 'карту'
            s += ' ('
            x = json_string["task_num"]
            if x == 1:
                s += json_string["task_name"][0]
                s += ', проект - ' + json_string["project_name"][0]
            else:
                for i in range(x):
                    temp = json_string["price"][i]
                    if x != 1:
                        s = s + str(temp) + ' '
                    s = s + str(json_string["task_name"][i])
                    s1 = json_string["project_name"][i]
                    if s1 != '-':
                        s = s + ', проект - ' + s1
                    if i != x - 1:
                        s = s + ' + '
            s += ')\nПожалуйста, подтвердите наличие перевода'
            await bot.send_message(user_id, 'Отлично, высылаю сообщение.. ')
            await bot.send_message(user_id, s)
            json_config_1 = open("config.json", "r", encoding="utf-8")
            json_file_1 = json.load(json_config_1)
            s1 = json_file_1["list_employee_tg"][json_file_1["list_employee_names"].index(json_string["employee_name"])]
            json_config_1.close()
            if s1 != '':
                s1 = 'Вот ник данного сотрудника: ' + s1
            else:
                s1 = 'Ника для данного сотрудника нет в системе :('
            await bot.send_message(user_id, s1, reply_markup=kb.inline_kb_after_json)
            users[user_id].stage = Stage.NONE
        else:
            await bot.send_message(user_id, "Что-то не то..")

    elif users[user_id].stage == Stage.EDIT_NAME:  # -------------------------------------------- EDIT_NAME -----------
        m_t = m_t[0].upper() + m_t[1:]
        json_config_1 = open("config.json", "r", encoding="utf-8")
        json_file_1 = json.load(json_config_1)
        json_file_1["list_employee_names"][users[user_id].edit_us_num] = m_t
        json_config_1.close()
        json_config_1 = open("config.json", "w", encoding="utf-8")
        json.dump(json_file_1, json_config_1, ensure_ascii=False, indent=3)
        json_config_1.close()
        await bot.send_message(user_id,
                               'Информация о сотруднике обновлена. Что дальше? 🌿', reply_markup=kb.inline_kb_main)
        users[user_id].stage = Stage.NONE
    elif users[user_id].stage == Stage.EDIT_TG:  # ------------------------------------------------ EDIT_TG -----------
        if m_t[0] == '@':
            json_config_1 = open("config.json", "r", encoding="utf-8")
            json_file_1 = json.load(json_config_1)
            json_file_1["list_employee_tg"][users[user_id].edit_us_num] = m_t
            json_config_1.close()
            json_config_1 = open("config.json", "w", encoding="utf-8")
            json.dump(json_file_1, json_config_1, ensure_ascii=False, indent=3)
            json_config_1.close()
            await bot.send_message(user_id,
                                   'Информация о сотруднике обновлена. Что дальше? 🌿', reply_markup=kb.inline_kb_main)
            users[user_id].stage = Stage.NONE
        else:
            await bot.send_message(user_id, 'Введите ник сотрудника в telegram в формате \n@name')

    else:  # ----------------------------------------------------------------------------------------- else -----------
        print (users[user_id].stage)
        await bot.send_message(user_id,
                               'Введите /start чтобы начать сставлять задание по переводу\nВведите /help для вывода '
                               'информации о боте')


# ----------------------------------------------------- BUTTONS ------------------------------------------------------

# employee names list of buttons -------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('b_s'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data[3:]
    if code.isdigit():
        code = int(code)
        if users[user_id].stage == Stage.EMPLOYEE_EDIT:
            s = 'Данные сотрудника:\n\nимя:   '
            json_config_1 = open("config.json", "r", encoding="utf-8")
            json_file_1 = json.load(json_config_1)
            s += json_file_1["list_employee_names"][code] + '\nбанк:   '
            s += json_file_1["list_employee_cards"][code] + '\ntelegram:   '
            s += json_file_1["list_employee_tg"][code] + '\n\nЧто вы хотите изменить для данного сотрудника?'
            json_config_1.close()
            users[user_id].edit_us_num = code
            await bot.send_message(callback_query.from_user.id, s, reply_markup=kb.inline_kb_edit)
        else:
            json_config_1 = open("config.json", "r", encoding="utf-8")
            json_file_1 = json.load(json_config_1)
            employee = json_file_1["list_employee_names"]
            bank = json_file_1["list_employee_cards"]
            json_config_1.close()
            users[user_id].Task.set_employee_name(employee[code])
            users[user_id].Task.set_employee_bank(bank[code])
            users[user_id].stage = Stage.TASK_NUM
            await bot.send_message(callback_query.from_user.id, 'Введите количество задач для данного сотрудника')
    else:
        print('ERROR 1')


# edit employee info -------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('edit'))
async def process_callback_edit_empl_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data[5:]
    if code == 'bank':
        users[user_id].stage = Stage.EDIT_BANK
        await bot.send_message(user_id, 'Выберите новый банк сотрудника: ', reply_markup=kb.inline_kb_banks)
    elif code == 'name':
        users[user_id].stage = Stage.EDIT_NAME
        await bot.send_message(user_id, 'Введите новое имя: ')
    else:
        users[user_id].stage = Stage.EDIT_TG
        await bot.send_message(user_id, 'Введите ник сотрудника в telegram в формате \n@name')


# if payment already exists -------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('exists'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    if code == 'exists_new_full':
        users[user_id].Task.set_already_exists(buh.AlreadyExists.NEW_FULL)
        users[user_id].Task.set_skip_exists_price()
        users[user_id].stage = Stage.PROJECT_NAME
        await bot.send_message(callback_query.from_user.id, 'Введите название проекта ' + str(users[user_id].qur_task))
    elif code == 'exists_new_part':
        users[user_id].Task.set_already_exists(buh.AlreadyExists.NEW_PARTIALLY)
        users[user_id].stage = Stage.IF_EXISTS
        await bot.send_message(callback_query.from_user.id, 'Введите полную сумму будущей оплаты: ')
    else:
        users[user_id].Task.set_already_exists(buh.AlreadyExists.OLD_PARTIALLY)
        users[user_id].Task.set_skip_exists_price()
        users[user_id].stage = Stage.PROJECT_NAME
        await bot.send_message(callback_query.from_user.id, 'Введите название проекта ' + str(users[user_id].qur_task))


# task and project links ----------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('butt'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    if users[user_id].stage == Stage.TASK_LINK:  # ---------------------------------------------- TASK_LINK -----------
        if code == 'butt2':
            users[user_id].Task.set_task_link('добавить новую')
        else:
            users[user_id].Task.set_task_link('нет ссылки')
        users[user_id].stage = Stage.PROJECT_LINK
        await bot.send_message(callback_query.from_user.id, 'Введите ссылку на проект. Если у вас нет ссылки, '
                                                            'нажмите на кнопку', reply_markup=kb.inline_kb_links1)

    else:  # --------------------------------------------------------------------------------- PROJECT_LINK -----------
        users[user_id].Task.set_project_link('нет ссылки')
        if int(users[user_id].qur_task) == int(users[user_id].tasks_in_total):
            await bot.send_message(callback_query.from_user.id, 'Все поля заполнены, высылаю готовое сообщение...')
            await bot.send_message(callback_query.from_user.id, users[user_id].Task.compose_a_message(),
                                   reply_markup=kb.inline_kb_send_msg)
            users[user_id].stage = Stage.NONE
        else:
            users[user_id].stage = Stage.PRICE
            users[user_id].qur_task += 1
            await bot.send_message(callback_query.from_user.id,
                                   'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))


# final send to Black_buh chat ----------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'bsend')
async def process_callback_button1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if users[user_id].stage == Stage.GET_NEW_EMPL_INFO:  # ------------------------------ GET_NEW_EMPL_INFO -----------
        # 243083696 is Alexa's chat
        await bot.send_message(-761980818, users[user_id].get_info_message)
        create_user_session(user_id)

    else:  # ----------------------------------------------------------------------------------------- NONE -----------
        print(users[user_id].Task.get_json())
        await bot.send_message(-761980818, users[user_id].Task.message)
        await bot.send_message(-761980818, users[user_id].Task.get_json())
        create_user_session(user_id)
    await bot.send_message(user_id,
                           'Сообщение отправлено! Что будем делать дальше? 🌿',
                           reply_markup=kb.inline_kb_main)


# back to main menu ---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def process_callback_back_to_main(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(user_id,
                           'Хорошо, мы в главном меню. Что будем делать? 🌿',
                           reply_markup=kb.inline_kb_main)


# main menu -----------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('new'))
async def process_callback_main_menu (callback_query: types.CallbackQuery):
    code = callback_query.data
    user_id = callback_query.from_user.id
    if code == 'new_task':
        users[user_id].stage = Stage.EMPLOYEE_NAME
        await bot.send_message(user_id,
                               'Введите первую букву фамилии сотрудника, которому необходимо отправить оплату')
    elif code == 'new_empl':
        users[user_id].stage = Stage.NONE
        await bot.send_message(user_id,
                               'Необходимо иметь Фамилию нового сотрудника. Если она у вас есть, введите её. Если нет'
                               ' - нажмите на кнопку, чтобы вернуться назад. Пожалуйста, будьте внимательны! '
                               'Функционал удаления сотрудника через бота пока не реализован :)',
                               reply_markup =kb.inline_kb_back_to_menu)
        users[user_id].stage = Stage.NEW_EMPLOYEE_NAME
    elif code == 'new_empl_message':
        users[user_id].Task.set_employee_name('новый')
        users[user_id].stage = Stage.TASK_NUM
        await bot.send_message(callback_query.from_user.id, 'Введите количество задач для нового сотрудника')
    elif code == 'new_message':
        await bot.send_message(user_id,
                               "Хорошо! Давай ка мне json...")
        users[user_id].stage = Stage.GETTING_MESSAGE
    elif code == 'new_edit':
        users[user_id].stage = Stage.EMPLOYEE_EDIT
        await bot.send_message(user_id,
                               'Введите первую букву фамилии сотрудника: ')
    else:
        users[user_id].stage = Stage.GET_NEW_EMPL_INFO
        await bot.send_message(user_id,
                               'Хорошо, напишите сообщение, которое вы хотите отправить. Можете не писать @alexa_ak, '
                               'я сделаю это сам.')


# new employee banks -------------------------------------------------------------------------------------------------
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bank'))
async def process_callback_new_empl_banks(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    bank = ''
    if code == 'bank_cancel':
            users[user_id].stage = Stage.NONE
            await bot.send_message(user_id,
                                   'Хорошо, мы в главном меню. Что будем делать? 🌿',
                                   reply_markup=kb.inline_kb_main)
    if users[user_id].stage == Stage.NEW_EMPLOYEE_BANK or users[user_id].stage == Stage.EDIT_BANK:
        if code == "bank_tink":
            bank = 'Тинькофф'
        elif code == 'bank_sber':
            bank = 'Сбер'
        elif code == 'bank_umoney':
            bank = 'Юмани'
        elif code == 'bank_other':
            bank = 'карту'
        json_config_1 = open("config.json", "r", encoding="utf-8")
        json_file_1 = json.load(json_config_1)
        if users[user_id].stage == Stage.NEW_EMPLOYEE_BANK:  # -------------------------- NEW_EMPLOYEE_BANK -----------
            json_file_1["list_employee_names"].insert(0, users[user_id].new_us_name)
            json_file_1["list_employee_cards"].insert(0, bank)
            json_config_1.close()
            json_config_1 = open("config.json", "w", encoding="utf-8")
            json.dump(json_file_1, json_config_1, ensure_ascii=False, indent=3)
            json_config_1.close()
            await bot.send_message(user_id,
                                   'Спасибо, сотрудник добавлен! Что дальше? 🌿', reply_markup=kb.inline_kb_main)
            users[user_id].stage = Stage.NONE
        else:  # -------------------------------------------------------------------------------- EDIT_BANK -----------
            json_file_1["list_employee_cards"][users[user_id].edit_us_num] = bank
            json_config_1.close()
            json_config_1 = open("config.json", "w", encoding="utf-8")
            json.dump(json_file_1, json_config_1, ensure_ascii=False, indent=3)
            json_config_1.close()
            await bot.send_message(user_id,
                                   'Информация о сотруднике обновлена. Что дальше? 🌿', reply_markup=kb.inline_kb_main)
            users[user_id].stage = Stage.NONE


if __name__ == '__main__':
    executor.start_polling(dp)

# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!", reply_markup=kb.greet_kb)

# @dp.message_handler(commands=['1'])
# async def process_command_1(message: types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)
#
# @dp.message_handler(commands=['2'])
# async def process_command_2(message: types.Message):
#     await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)

# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


# @dp.callback_query_handler(lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
#
# @dp.callback_query_handler(lambda c: c.data == 'button2')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата вторая кнопка!')
