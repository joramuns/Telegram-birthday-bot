# -*- coding: utf-8 -*-
import telebot
from telebot.types import BotCommand
import re, time
import config, sqlite_bot, bd_next, bd
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
    # Cut version for big data
    array_words = message.text.split()
    if (len(array_words) > 2):
        bot.send_message(message.chat.id, "Нужно ввести команду и через пробел дату без лишних слов!", reply_to_message_id=config.manual_thread_id)
        return

    if (len(array_words) == 2):
        get_num_month = [n for n, x in enumerate(config.monthes) if array_words[1] in x]
        if len(get_num_month) == 0:
            bot.send_message(message.chat.id, "Либо месяца такого нет у нас в архивах, либо тебе русский язык стоит подучить!", reply_to_message_id=config.manual_thread_id)
            return
        else:
            s_month = "where bd_month = " + str(get_num_month[0] + 1)
            birthday_list = sqlite_bot.bd_list(message, s_month, 0)
    else:
        message_out = "Моя русский не дружил, а дня рожденя в этом чате:\n"
        for i in range(len(config.monthes) + 1):
            s_month = "where bd_month = " + str(i)
            birthday_list = sqlite_bot.bd_list(message, s_month, 1)
            if birthday_list[0][0]:
                message_out = message_out + config.seasons[i - 1] + " <b>" + str(birthday_list[0][0]) + "</b> штук для " + str(config.monthes[i - 1]) + "\n"
        bot.send_message(message.chat.id, message_out, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)
        return

    if not birthday_list:
        bot.send_message(message.chat.id, "Список дней рождения еще пуст", reply_to_message_id=config.manual_thread_id)
        return
    birthday_list_sorted = ['', '', '']
    message_list = "Вот такие у нас именниники в чате:\n"
    time_now = time.localtime()

    for i in range(len(birthday_list)):

        # Дата рождения позади
        if (time_now.tm_mon > birthday_list[i][4]) or (time_now.tm_mon == birthday_list[i][4] and time_now.tm_mday > birthday_list[i][3]):
            if (birthday_list[i][5] == 0):
                str_age = ", про возраст история умалчивает.\n"
            else:
                str_age = " и исполнится {}.\n".format(time_now.tm_year - birthday_list[i][5] + 1)
            birthday_list_sorted[2] += "\n{}<b>{}</b> отмечает {} {}".format(config.seasons[birthday_list[i][4]-1], birthday_list[i][2], birthday_list[i][3], config.monthes[birthday_list[i][4]-1]) + str_age

        # Дата рождения впереди
        if (time_now.tm_mon < birthday_list[i][4]) or (time_now.tm_mon == birthday_list[i][4] and time_now.tm_mday < birthday_list[i][3]):
            if (birthday_list[i][5] == 0):
                str_age = " и возраст является секретиком.\n"
            else:
                str_age = " и исполнится {}.\n".format(time_now.tm_year - birthday_list[i][5])
            birthday_list_sorted[1] += "\n{}<b>{}</b> отмечает {} {}".format(config.seasons[birthday_list[i][4]-1], birthday_list[i][2], birthday_list[i][3], config.monthes[birthday_list[i][4]-1]) + str_age

        # Сегодня день рождения
        if time_now.tm_mon ==  birthday_list[i][4] and time_now.tm_mday == birthday_list[i][3]:
            if (birthday_list[i][5] == 0):
                str_age = " Сколько исполнилось - пусть скажет именинник!"
            else:
                str_age = "С " + str(time_now.tm_year - birthday_list[i][5]) + " летием, " + birthday_list[i][2] + "!!!"
            birthday_list_sorted[0] = birthday_list_sorted[0] + "\n\U0001F389 Сегодня, " + str(birthday_list[i][3]) + " " + config.monthes[birthday_list[i][4]-1] + ", у <b>" + birthday_list[i][2] + "</b> день рождения! "  + str_age


    message_list = message_list + birthday_list_sorted[0] + birthday_list_sorted[1] + birthday_list_sorted[2]

    bot.send_message(message.chat.id, message_list, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

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
