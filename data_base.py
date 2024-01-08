import json


def open_json_file_and_write():
    with open("users.json", encoding="utf-8") as file:
        date = json.load(file)
    return date


def save_json_file_and_write(date):
    with open('users.json', 'w', encoding='utf-8') as outfile:
        json.dump(date, outfile, ensure_ascii=False, indent=4)


def start_json_file(message):
    with open("users.json", encoding="utf-8") as file:
        date = json.load(file)
    date["users"][message.chat.username] = {}
    with open('users.json', 'w', encoding='utf-8') as outfile:
        json.dump(date, outfile, ensure_ascii=False, indent=4)


def write_in_json_file_default_arg(message, arg, value):
    with open("users.json", encoding="utf-8") as file:
        date = json.load(file)
        date["users"][message.chat.username][arg] = value
        with open('users.json', 'w', encoding='utf-8') as outfile:
            json.dump(date, outfile, ensure_ascii=False, indent=4)