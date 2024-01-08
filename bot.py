import telebot
import json
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import *
from info import Question
from info import questions_list,task_list,score_list
token="6907428347:AAEtzb1VtogJOP5zTZ2GuLbI1V2NgUwOMWo"

#https://t.me/testspider_bot
bot = telebot.TeleBot(token=token)



def markup_create(question):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(question.task)):
        markup.add(types.KeyboardButton(question.task[i]))
    return markup


def question_create_from_class(message, date):
    question = Question(questions_list[date["users"][message.chat.username]["index"]],
                        task_list[date["users"][message.chat.username]["index"]])
    return question



@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.from_user.id,"Чтобы начать тест вызови /start.\n Перед тобой появятся вопросы и ниже варианты ответов")


@bot.message_handler(commands=['start'])
def start(message):
    start_json_file(message)
    write_in_json_file_default_arg(message, "index", 0)
    write_in_json_file_default_arg(message, "score", 0)
    date = open_json_file_and_write()
    question = question_create_from_class(message, date)
    markup = markup_create(question)
    bot.send_message(chat_id=message.chat.id, text=f"Привет,{message.from_user.first_name}. Держи тестик насколько ты человек паук:", reply_markup=markup)
    msg = bot.reply_to(message, f"Первый вопрос:\n{question.question}")
    bot.register_next_step_handler(message, processing_user_response)


def processing_user_response(message):
    date = open_json_file_and_write()
    question = question_create_from_class(message, date)
    if message.text in question.task:
        date["users"][message.chat.username]["score"] += score_list[question.task.index(message.text)]
        date["users"][message.chat.username]["index"] += 1
        bot.send_message(chat_id=message.chat.id,
                         text="Ответ принят!",
                         reply_markup=types.ReplyKeyboardRemove())
        save_json_file_and_write(date)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы написали фуфню, переходим к след. вопросу",
                         reply_markup=types.ReplyKeyboardRemove())
        date["users"][message.chat.username]["index"] += 1
        save_json_file_and_write(date)
    if date["users"][message.chat.username]["index"] == len(questions_list):
        bot.send_message(chat_id=message.chat.id,
                         text=f"Вы человек паук на: {round(date['users'][message.chat.username]['score'] / 16, 2) * 100}%"
                              "\n (Можешь попробовать заново по команде /start)")
        if  14 <= date["users"][message.chat.username]["score"] <= 16:
            bot.send_message(chat_id=message.chat.id, text="ВАУ! Питер паркер, это ты? ")
            bot.send_photo(message.chat.id,"https://i.pinimg.com/564x/75/1b/9a/751b9a98a29c605f70ef79db4d8d830d.jpg")
        elif 11 <= date["users"][message.chat.username]["score"] <= 13:
            bot.send_message(chat_id=message.chat.id, text="Хм, потенциал в тебе есть. Поработай ещё чуть чуть")
            bot.send_photo(message.chat.id, "https://i.pinimg.com/736x/fd/82/67/fd82676567114f058863dccdbb12f483.jpg")
        elif 8 <= date["users"][message.chat.username]["score"] <= 10:
            bot.send_message(chat_id=message.chat.id, text="возможно в тебе есть далёёёкие гены человека паука")
            bot.send_photo(message.chat.id, "https://i.pinimg.com/564x/f1/f8/fb/f1f8fb63066b313c877d57d3394f24a4.jpg")
        elif 4 <= date["users"][message.chat.username]["score"] <= 7:
            bot.send_message(chat_id=message.chat.id, text="И ты называешь себя человеком пауком?")
            bot.send_photo(message.chat.id, "https://i.pinimg.com/564x/50/56/30/505630b0eb651c17a96b355914045dd3.jpg")

    else:
        question = question_create_from_class(message, date)
        markup = markup_create(question)
        bot.send_message(chat_id=message.chat.id, text="Следующий вопрос:", reply_markup=markup)
        msg = bot.reply_to(message, text=question.question)
        bot.register_next_step_handler(msg, processing_user_response)


@bot.message_handler(content_types=['text'])
def incorrect_input(message):
    bot.send_message(chat_id=message.chat.id,
                     text=f"Пройдите опрос по команде: /start")

bot.polling()