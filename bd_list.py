import sqlite_bot, time, config

def output(message):
    # Cut version for big data
    array_words = message.text.split()
    if (len(array_words) > 2):
        return "Нужно ввести команду и через пробел дату без лишних слов!"

    if (len(array_words) == 2):
        get_num_month = [n for n, x in enumerate(config.monthes) if array_words[1] in x]
        if len(get_num_month) == 0:
            return "Либо месяца такого нет у нас в архивах, либо тебе русский язык стоит подучить!"
        else:
            message_out = month_list(get_num_month, message.from_user.id)
            return message_out
    else:
        message_out = common_list(message.from_user.id)
        return message_out

    if not birthday_list:
        return "Список дней рождения еще пуст"


def common_list(user_id):
    message_out = "Количество именинников в каждом месяце:\n"
    for i in range(len(config.monthes) + 1):
        s_month = "where bd_month = " + str(i)
        birthday_list = sqlite_bot.bd_list(config.manual_chat_id, user_id, s_month, 1)
        if birthday_list[0][0]:
            message_out = message_out + config.seasons[i - 1] + " <b>" + str(birthday_list[0][0]) + "</b> штук для " + str(config.monthes[i - 1]) + "\n"

    return message_out

def month_list(get_num_month, user_id):
    s_month = "where bd_month = " + str(get_num_month[0] + 1)
    birthday_list = sqlite_bot.bd_list(config.manual_chat_id, user_id, s_month, 0)

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

    return message_list
