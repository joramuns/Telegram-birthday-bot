import re, time
import config, sqlite_bot

def output(message):
    array_words = message.text.split()
    pattern_birthday = "([0-9]{2})\.([0-9]{2})\.([0-9]{4})$"
    pattern_birthday2 = "([0-9]{2})\.([0-9]{2})$"
    if (len(array_words) > 2):
        return "Нужно ввести команду и через пробел дату без лишних слов!"

    if (len(array_words) == 1):
        check_register = sqlite_bot.check_bd(message)
        if check_register:
            message_done = check_register[0][2] + " родился " + str(check_register[0][3]) + " " + config.monthes[check_register[0][4]-1]
            if check_register[0][5] == 0:
                message_done = message_done + " неизвестно какого года."
            else:
                message_done = message_done + " " + str(check_register[0][5]) + " года!"
            return message_done
        else:
            return "Необходимо ввести команду\n/birthday и через пробел дату рождения в формате ДД.ММ.ГГГГ или ДД.ММ, если есть что скрывать"

    birthdate = array_words[1]

    if not re.match(pattern_birthday, birthdate) and not re.match(pattern_birthday2, birthdate):
        return "Формат даты принимается только в таких видах - 00.00.0000 или 00.00"

    day = birthdate[:2]
    month = birthdate[3:5]
    if re.match(pattern_birthday, birthdate):
        year = birthdate[6:]
    else:
        year = '0'

    if int(day) < 1 or int(day) > 31:
        return "Такого дня не может быть"

    if int(month) < 1 or int(month) > 12:
        return "В году 12 месяцев, вообще-то"

    if (year == '0000'):
        return "А ты француз, бом бом бом!"

    if ((int(year) > time.localtime().tm_year - 1) or int(year) < 1922) and (int(year) != 0):
        return "Ну не может быть такого года рождения, что за вздор"

    if (int(year) == time.localtime().tm_year and int(month) >= time.localtime().tm_mon and int(day) > time.localtime().tm_mday):
        return "Аларм! В чате гость из будущего!"

    if int(day) > config.monthes_length[int(month)-1]:
        if (int(month) == 2 and int(year) != 0):
            if (int(year) % 4 != 0):
                return "Это не високосный год, какое "+ day +"-е февраля!?"
        else:
            return "А нет столько дней в этом месяце!"

    if int(month) == 2 and int(day) > 29:
        return "Нет столько дней в этом феврале!"

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

    return message_done
