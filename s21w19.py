# -*- coding: utf-8 -*-
import telebot
from telebot.types import BotCommand
import re, time
import config, sqlite_bot
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
    birthday_list = sqlite_bot.bd_list(message, "", 0)
    if not birthday_list:
        bot.send_message(message.chat.id, "Список дней рождений еще пуст", reply_to_message_id=manual_thread_id)
        return
    birthday_next = ['0', '0', '0', '0', '0', '0']
    message_next = "Ближайший день рождения в чате у:\n"
    time_now = time.localtime()

    # Проверка этого года после сегодня
    for i in range(len(birthday_list)):

        # Сегодня день рождения
        if time_now.tm_mon ==  birthday_list[i][4] and time_now.tm_mday == birthday_list[i][3]:
            if (birthday_list[i][5] == 0):
                str_age = " Сколько исполнилось - пусть скажет именинник! \U0001F38A"
            else:
                str_age = "С " + str(time_now.tm_year - birthday_list[i][5]) + " летием, " + birthday_list[i][2] + "!!! \U0001F388"
            message_next = message_next + "\n\U0001F389 Сегодня, " + str(birthday_list[i][3]) + " " + config.monthes[birthday_list[i][4]-1] + ", у <b>" + birthday_list[i][2] + "</b> день рождения! \U0001F381 "  + str_age

        if ((time_now.tm_mon == birthday_list[i][4] and time_now.tm_mday < birthday_list[i][3]) or time_now.tm_mon < birthday_list[i][4]):
            if (birthday_next[3] != birthday_list[i][3] or birthday_next[4] != birthday_list[i][4]) and (birthday_next[0] != '0'):
                break
            birthday_next = birthday_list[i]
            message_next = message_next + "\n\U000023F3 <b>" + birthday_next[2] + "</b> празднует " + str(birthday_next[3]) + " " + config.monthes[birthday_next[4]-1]

    # Если ничего не нашлось, проверка следующего года
    if birthday_next[0] == '0':
        for i in range(len(birthday_list)):
            if (birthday_next[3] != birthday_list[i][3] or birthday_next[4] != birthday_list[i][4]) and (birthday_next[0] != '0'):
                break
            birthday_next = birthday_list[i]
            message_next = message_next + "\nВ следующем году " + birthday_next[2] + " празднует " + str(birthday_next[3]) + " " + config.monthes[birthday_next[4]-1]

    bot.send_message(message.chat.id, message_next, reply_to_message_id=manual_thread_id, parse_mode="HTML")

@bot.message_handler(commands=["днюхи", "birthday_list"])
def birthday_list(message):
    # Cut version for big data
    array_words = message.text.split()
    if (len(array_words) > 2):
        bot.send_message(message.chat.id, "Нужно ввести команду и через пробел дату без лишних слов!", reply_to_message_id=manual_thread_id)
        return

    if (len(array_words) == 2):
        get_num_month = [n for n, x in enumerate(config.monthes) if array_words[1] in x]
        if len(get_num_month) == 0:
            bot.send_message(message.chat.id, "Либо месяца такого нет у нас в архивах, либо тебе русский язык стоит подучить!", reply_to_message_id=manual_thread_id)
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
        bot.send_message(message.chat.id, message_out, parse_mode="HTML", reply_to_message_id=manual_thread_id)
        return

    if not birthday_list:
        bot.send_message(message.chat.id, "Список дней рождения еще пуст", reply_to_message_id=manual_thread_id)
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

    bot.send_message(message.chat.id, message_list, parse_mode="HTML", reply_to_message_id=manual_thread_id)

@bot.message_handler(commands=["днюха", "birthday"])
def birthday(message):
    array_words = message.text.split()
    pattern_birthday = "([0-9]{2})\.([0-9]{2})\.([0-9]{4})$"
    pattern_birthday2 = "([0-9]{2})\.([0-9]{2})$"
    if (len(array_words) > 2):
        bot.send_message(message.chat.id, "Нужно ввести команду и через пробел дату без лишних слов!", reply_to_message_id=manual_thread_id)
        return

    if (len(array_words) == 1):
        check_register = sqlite_bot.check_bd(message)
        if check_register:
            message_done = check_register[0][2] + " родился " + str(check_register[0][3]) + " " + config.monthes[check_register[0][4]-1]
            if check_register[0][5] == 0:
                message_done = message_done + " неизвестно какого года."
            else:
                message_done = message_done + " " + str(check_register[0][5]) + " года!"
            bot.send_message(message.chat.id, message_done, reply_to_message_id=manual_thread_id)
            return
        else:
            bot.send_message(message.chat.id, "Необходимо ввести команду\n/birthday и через пробел дату рождения в формате ДД.ММ.ГГГГ или ДД.ММ, если есть что скрывать", reply_to_message_id=manual_thread_id)
        return

    birthdate = array_words[1]

    if not re.match(pattern_birthday, birthdate) and not re.match(pattern_birthday2, birthdate):
        bot.send_message(message.chat.id, "Формат даты принимается только в таких видах - 00.00.0000 или 00.00", reply_to_message_id=manual_thread_id)
        return

    day = birthdate[:2]
    month = birthdate[3:5]
    if re.match(pattern_birthday, birthdate):
        year = birthdate[6:]
    else:
        year = '0'

    if int(day) < 1 or int(day) > 31:
        bot.send_message(message.chat.id, "Такого дня не может быть", reply_to_message_id=manual_thread_id)
        return

    if int(month) < 1 or int(month) > 12:
        bot.send_message(message.chat.id, "В году 12 месяцев, вообще-то", reply_to_message_id=manual_thread_id)
        return

    if (year == '0000'):
        bot.send_message(message.chat.id, "А ты француз, бом бом бом!", reply_to_message_id=manual_thread_id)
        return

    if ((int(year) > time.localtime().tm_year - 1) or int(year) < 1922) and (int(year) != 0):
        bot.send_message(message.chat.id, "Ну не может быть такого года рождения, что за вздор", reply_to_message_id=manual_thread_id)
        return

    if (int(year) == time.localtime().tm_year and int(month) >= time.localtime().tm_mon and int(day) > time.localtime().tm_mday):
        bot.send_message(message.chat.id, "Аларм! В чате гость из будущего!", reply_to_message_id=manual_thread_id)
        return

    if int(day) > config.monthes_length[int(month)-1]:
        if (int(month) == 2 and int(year) != 0):
            if (int(year) % 4 != 0):
                bot.send_message(message.chat.id, "Это не високосный год, какое "+ day +"-е февраля!?", reply_to_message_id=manual_thread_id)
                return
        else:
            bot.send_message(message.chat.id, "А нет столько дней в этом месяце!", reply_to_message_id=manual_thread_id)
            return

    if int(month) == 2 and int(day) > 29:
        bot.send_message(message.chat.id, "Нет столько дней в этом феврале!", reply_to_message_id=manual_thread_id)
        return

    if not message.from_user.username:
        message.from_user.username = '0'

    check_register = sqlite_bot.check_bd(message)
    if (check_register):
        sqlite_bot.change_bd(message, day, month, year)
        message_done = "Меняю дату рождения пользователя " + check_register[0][2] + " с " + str(check_register[0][3]) + " " + config.monthes[check_register[0][4]-1]
        if check_register[0][5] == 0:
            message_done = message_done + " на "
        else:
            message_done = message_done + " " + str(check_register[0][5]) + " года на "
        message_done = message_done + day + " " + config.monthes[int(month)-1]
        if year == '0':
            message_done = message_done + "."
        else:
            message_done = message_done + " " + year + " года."

    else:
        sqlite_bot.add_bd(message, day, month, year)
        message_done = "Внесу в блокнот, что " + message.from_user.first_name + " родился(-ась) " + day + " " + config.monthes[int(month)-1]
        if year == '0':
            message_done = message_done + " , а возраст будет секретиком."
        else:
            message_done = message_done + " , в " + year + " году."

    bot.send_message(message.chat.id, message_done, parse_mode="HTML", reply_to_message_id=manual_thread_id)

@bot.message_handler(commands=["помощь"])
def helpmenu(message):
    bot.send_message(message.chat.id, "<b>Инструкция по днюхоботу:</b>\n\n- <b>\"/днюха ДД.ММ.ГГГГ\"</b> - установить свою дату рождения в формате ДД.ММ.ГГГГ или ДД.ММ\n- <b>\"/днюха\"</b> - посмотреть какую дату рождения будет отображать бот у тебя\n- <b>\"/днюхи\"</b> - посмотреть сколько именниников в каждом месяце в этом чате\n- <b>\"/днюхи января\"</b> - посмотреть какие дни рождения в январе (или в другом месяце, указывать в родительном падеже)\n- <b>\"/ближайшаяднюха\"</b> - покажет кто скоро проставляется!", parse_mode="HTML", reply_to_message_id=manual_thread_id)

event_job = threading.Event()
def job_handler():
    while not event_job.is_set():
        if (last_message):
            job_message="Посмотрим-ка, что там у нас в календаре..."
            bot.send_message(manual_chat_id, job_message, reply_to_message_id=manual_thread_id)
            birthday_next(last_message)
        else:
            job_message="Ох, опять разбудили! \U000023F0"
            bot.send_message(manual_chat_id, job_message, reply_to_message_id=manual_thread_id)
        event_job.wait(43200)

job_thread = threading.Thread(target=job_handler)
job_thread.start()

bot.polling(none_stop=True, interval=1)

event_job.set()
job_thread.join()
