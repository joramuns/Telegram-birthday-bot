import sqlite_bot, time, config, datetime

def count_days(chat_id, user_id):
    birthday_list = sqlite_bot.bd_list(chat_id, user_id, "", 0)
    if not birthday_list:
        return "Список дней рождений еще пуст"

    now = datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    min_this_year = 365
    max_next_year = -min_this_year

    for item in birthday_list:
        birthdate = datetime.datetime(year=now.year, month=item[4], day=item[3])
        days_left = (birthdate - now).days
        if days_left == 0:
            return 0
        elif days_left > 0 and days_left < min_this_year:
            min_this_year = days_left
        elif days_left < 0 and days_left > max_next_year:
            max_next_year = days_left

    if min_this_year == 365:
        return -max_next_year
    else:
        return min_this_year

def output(chat_id, user_id):
    birthday_list = sqlite_bot.bd_list(chat_id, user_id, "", 0)
    if not birthday_list:
        return "Список дней рождений еще пуст"
    birthday_next = ['0', '0', '0', '0', '0', '0']
    message_next = "Ближайший день рождения в чате у:\n"
    time_now = time.localtime()

    # Проверка этого года после сегодня
    for i in range(len(birthday_list)):

        # Сегодня день рождения
        if time_now.tm_mon ==  birthday_list[i][4] and time_now.tm_mday == birthday_list[i][3]:
            if (birthday_list[i][5] == 0):
                str_age = " Сколько исполнилось - пусть скажет именинник! \U0001F38A \n"
            else:
                str_age = "С " + str(time_now.tm_year - birthday_list[i][5]) + " летием, " + birthday_list[i][2] + "!!! \U0001F388 \n"
            message_next = message_next + "\n\U0001F389 Сегодня, " + str(birthday_list[i][3]) + " " + config.monthes[birthday_list[i][4]-1] + ", у <b>" + birthday_list[i][2] + " (@" + birthday_list[i][1] +")</b> день рождения! \U0001F381 "  + str_age
            birthday_next = birthday_list[i]

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
    return message_next
