# -*- coding: utf-8 -*-
import telebot
from telebot.types import BotCommand
import re, time
import config, sqlite_bot, bd_next, bd, bd_list
import threading
#temp
import random

bot = telebot.TeleBot(config.token);
global bot_state
bot_state = 0
bot_id = bot.get_me().id
last_message=""

@bot.message_handler(commands=["start"])
def start(message, res=False):
    if message.from_user.username != config.owner:
        bot.send_message(message.chat.id, 'Только мой господин может заводить меня')
        return
    global bot_state
    if bot_state == 0:
        bot.send_message(message.chat.id, 'Хозяин, я готов к работе')
        bot_state = bot_state + 1
    else:
        bot.send_message(message.chat.id, 'Хозяин, я уже в работе')

@bot.message_handler(commands=["stop"])
def stop(message):
    if message.from_user.username != config.owner:
        bot.send_message(message.chat.id, 'Только мой господин может остановить меня')
        return
    global bot_state
    if bot_state == 1:
        bot_state = bot_state - 1
        bot.send_message(message.chat.id, 'До новых встреч, неудачники!')

@bot.message_handler(commands=["ближайшаяднюха", "birthday_next"])
def birthday_next(message):
    global last_message
    if not last_message:
        last_message = message
        last_message.from_user.id = bot_id

    output_message = bd_next.output(message)
    bot.send_message(message.chat.id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")

@bot.message_handler(commands=["днюхи", "birthday_list"])
def birthday_list(message):
    output_message=bd_list.output(message)
    bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

@bot.message_handler(commands=["днюха", "birthday"])
def birthday(message):
    output_message = bd.output(message)
    bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

@bot.message_handler(commands=["помощь"])
def helpmenu(message):
    bot.send_message(message.chat.id, "<b>Инструкция по днюхоботу:</b>\n\n- <b>\"/днюха ДД.ММ.ГГГГ\"</b> - установить свою дату рождения в формате ДД.ММ.ГГГГ или ДД.ММ\n- <b>\"/днюха\"</b> - посмотреть какую дату рождения будет отображать бот у тебя\n- <b>\"/днюхи\"</b> - посмотреть сколько именниников в каждом месяце в этом чате\n- <b>\"/днюхи января\"</b> - посмотреть какие дни рождения в январе (или в другом месяце, указывать в родительном падеже)\n- <b>\"/ближайшаяднюха\"</b> - покажет кто скоро проставляется!", parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

event_job = threading.Event()
def job_handler():
    while not event_job.is_set():
        if (last_message):
            job_message="Посмотрим-ка, что там у нас в календаре..."
            bot.send_message(config.manual_chat_id, job_message, reply_to_message_id=config.manual_thread_id)
            birthday_next(last_message)
        else:
            job_message="Ох, опять разбудили! \U000023F0"
            bot.send_message(config.manual_chat_id, job_message, reply_to_message_id=config.manual_thread_id)
        event_job.wait(43200)

job_thread = threading.Thread(target=job_handler)
job_thread.start()

bot.polling(none_stop=True, interval=1)

event_job.set()
job_thread.join()
