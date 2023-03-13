import json
import os
os.chdir("../")

jsonConfig = open("config.json", "r", encoding="utf-8")
json_file = json.load(jsonConfig)

print(len(json_file['list_employee_tg']))
print(len(json_file['list_employee_names']))
print(len(json_file['list_employee_cards']))