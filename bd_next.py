import sqlite_bot, time, config

def output(message):
    birthday_list = sqlite_bot.bd_list(message, "", 0)
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
    return message_next
