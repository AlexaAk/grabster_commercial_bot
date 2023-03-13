from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# main menu -----------------------------------------------------------------------------------------------------------
inline_btn_empl = InlineKeyboardButton('Добавить нового сотрудника', callback_data='new_empl')
inline_btn_task = InlineKeyboardButton('Задание на перевод', callback_data='new_task')
inline_btn_empl_info = InlineKeyboardButton('Запросить данные о новом сотруднике', callback_data='new_empl_info')
inline_btn_empl_mess = InlineKeyboardButton('Перевод сотруднику, которого нет в боте', callback_data='new_empl_message')
inline_btn_message = InlineKeyboardButton('Создать сообщение по json', callback_data='new_message')
inline_btn_empl_edit = InlineKeyboardButton('Редактировать данные о сотруднике', callback_data='new_edit')

inline_kb_main = InlineKeyboardMarkup(row_width=2).add(inline_btn_task)
inline_kb_main.add(inline_btn_empl)
inline_kb_main.add(inline_btn_empl_mess)
inline_kb_main.add(inline_btn_empl_info)
inline_kb_main.add(inline_btn_message)
inline_kb_main.add(inline_btn_empl_edit)

# back to menu --------------------------------------------------------------------------------------------------------
inline_btn_back_to_menu = InlineKeyboardButton('Назад в меню', callback_data='back_to_main')

inline_kb_back_to_menu = InlineKeyboardMarkup().add(inline_btn_back_to_menu)

# if full transaction -------------------------------------------------------------------------------------------------
inline_btn_exists_1 = InlineKeyboardButton('Это новый полный перевод', callback_data='exists_new_full')
inline_btn_exists_2 = InlineKeyboardButton('Это новый частичный перевод', callback_data='exists_new_part')
inline_btn_exists_3 = InlineKeyboardButton('Это дополнение к старому переводу', callback_data='exists_old_part')

inline_kb_exists = InlineKeyboardMarkup(row_width=2).add(inline_btn_exists_1)
inline_kb_exists.add(inline_btn_exists_2)
inline_kb_exists.add(inline_btn_exists_3)

# task and project links ----------------------------------------------------------------------------------------------
inline_btn_1 = InlineKeyboardButton('Без ссылки', callback_data='butt1')
inline_btn_2 = InlineKeyboardButton('Добавить задачу', callback_data='butt2')

inline_kb_links1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_links2 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_links2.add(inline_btn_2)

# new employee banks -------------------------------------------------------------------------------------------------
inline_btn_tink = InlineKeyboardButton('Тинькофф', callback_data='bank_tink')
inline_btn_sber = InlineKeyboardButton('Сбер', callback_data='bank_sber')
inline_btn_other = InlineKeyboardButton('Другой', callback_data='bank_other')
inline_btn_umoney = InlineKeyboardButton('Юмани', callback_data='bank_umoney')
inline_btn_cancel = InlineKeyboardButton('ОТМЕНА', callback_data='bank_cancel')

inline_kb_banks = InlineKeyboardMarkup().add(inline_btn_tink)
inline_kb_banks.add(inline_btn_sber)
inline_kb_banks.add(inline_btn_umoney)
inline_kb_banks.add(inline_btn_other)
inline_kb_banks.add(inline_btn_cancel)

# edit employee info --------------------------------------------------------------------------------------------------
inline_btn_edit_name = InlineKeyboardButton('Изменить имя', callback_data='edit_name')
inline_btn_edit_bank = InlineKeyboardButton('Изменить банк (карту)', callback_data='edit_bank')
inline_btn_edit_tg = InlineKeyboardButton('Изменить ник в telegram', callback_data='edit_tg')

inline_kb_edit = InlineKeyboardMarkup().add(inline_btn_edit_name)
inline_kb_edit.add(inline_btn_edit_bank)
inline_kb_edit.add(inline_btn_edit_tg)
inline_kb_edit.add(inline_btn_back_to_menu)

# after sending json --------------------------------------------------------------------------------------------------
inline_kb_after_json = InlineKeyboardMarkup().add(inline_btn_message)
inline_kb_after_json.add(inline_btn_back_to_menu)

# final send to Black_buh chat ----------------------------------------------------------------------------------------
inline_btn_send_msg = InlineKeyboardButton('Отправить в чат с Бухгалтером', callback_data='bsend')

inline_kb_send_msg = InlineKeyboardMarkup(row_width=2).add(inline_btn_send_msg)

# employee buttons list -----------------------------------------------------------------------------------------------
stuff_kb_list = []


def fill_stuff_kb(stuff):
    stuff_kb = InlineKeyboardMarkup(row_width=2)
    for i in range(len(stuff[0])):
        stuff_kb.add(InlineKeyboardButton(stuff[0][i], callback_data='b_s' + str(stuff[1][i])))
        # print(buh.employee[stuff[1][i]] + '     ' + 'b_s' + str(stuff[1][i]))
    stuff_kb_list.append(stuff_kb)


def clean_stuff_kb():
    stuff_kb_list.clear()
