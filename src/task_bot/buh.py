from enum import Enum
import json


class Payment(Enum):
    PAID = 'Оплачено'
    PARTIALLY_PAID = 'Частично оплачено'
    UNPAID = 'Не оплачено'


class AlreadyExists(Enum):
    NEW_FULL = 1
    NEW_PARTIALLY = 2
    OLD_PARTIALLY = 3


class Task:
    def __init__(self):
        self.employee_name = ''
        self.employee_bank = ''
        self.task_num = 0
        self.total_price = 0
        self.price = []
        self.task_name = []

        self.already_exists = []
        self.if_exists_price = []

        self.project_name = []
        self.is_paid = []
        self.task_link = []
        self.project_link = []
        self.message = ''

    def compose_a_message (self):
        ans = 'Перевести:   ' + self.employee_name + ',   '
        for item in self.price:
            self.total_price += item
        ans += str(self.total_price) + '\n'
        ans += 'Количество задач: ' + str(self.task_num) + '\n'

        for i in range (self.task_num):
            s = ''
            if self.task_num != 1:
                s = str(self.price[i]) + ': ' + '\n'
            # print (self.task_name[i], self.project_name[i])
            s += '   Задача: ' + self.task_name[i]
            if self.task_link[i] != '':
                s += '  (' + self.task_link[i] + ')\n'
            else:
                s += '\n'
            s += '   Проект: ' + self.project_name[i]
            if self.project_link[i] != '':
                s += '  (' + self.project_link[i] + ')\n'
            else:
                s += '\n'
            if self.already_exists[i] == AlreadyExists.NEW_PARTIALLY:
                s += '   Новая, частичная оплата из ' + str(self.if_exists_price[i]) + '\n'
            elif self.already_exists[i] == AlreadyExists.OLD_PARTIALLY:
                s += '   Уже существует, частичная оплата\n'
            else:
                s += '   Новая, полная оплата\n'
            ans += s + '\n'
        self.message = ans
        return ans

    def set_already_exists (self, already_exists1):
        self.already_exists.append(already_exists1)

    def set_if_exists_price(self, if_exists_price1):
        self.if_exists_price.append(if_exists_price1)

    def set_skip_exists_price(self):
        self.if_exists_price.append(0)

    def set_employee_name (self, employee_name1):
        self.employee_name = employee_name1

    def set_employee_bank (self, employee_bank1):
        self.employee_bank = employee_bank1

    def inc_task_num (self):
        self.task_num += 1

    def set_task_num (self, task_num1):
        self.task_num = task_num1

    def set_price (self, price1):
        self.price.append(price1)

    def set_task_name (self, task_name1):
        self.task_name.append(task_name1)

    def set_project_name (self, project_name1):
        self.project_name.append(project_name1)

    def set_is_paid (self, is_paid1):
        self.is_paid.append(is_paid1)

    def set_task_link (self, task_link1):
        self.task_link.append(task_link1)

    def set_project_link (self, project_link1):
        self.project_link.append(project_link1)

    def get_employee_name (self):
        return self.employee_name

    def get_price(self):
        return self.price

    def get_task_name(self):
        return self.task_name

    def get_project_name(self):
        return self.project_name

    def get_is_paid(self):
        return self.is_paid

    def get_task_link(self):
        return self.task_link

    def get_project_link(self):
        return self.project_link

    def get_already_exists (self):
        return self.already_exists

    def get_if_exists_price(self):
        return self.if_exists_price

    def get_json(self):
        d = {'employee_name': self.employee_name, 'employee_bank': self.employee_bank, 'task_num': self.task_num,
             'total_price': self.total_price, 'price': self.price, 'task_name': self.task_name,
             'project_name': self.project_name}
        d_json = json.dumps(d, ensure_ascii=False)
        return d_json
