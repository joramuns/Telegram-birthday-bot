from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
import config

def button_setter(counter, owner):
    counter = int(counter)
    reply_markup = InlineKeyboardMarkup()
    cb_msg = concat_owner_month(config.monthes[counter], owner)
    button = InlineKeyboardButton(config.monthes[counter], callback_data=cb_msg)
    reply_markup.row(button)
    counter += 1
    cb_msg = concat_owner_month(config.monthes[counter], owner)
    button = InlineKeyboardButton(config.monthes[counter], callback_data=cb_msg)
    reply_markup.row(button)
    counter += 1
    cb_msg = concat_owner_month(config.monthes[counter], owner)
    button = InlineKeyboardButton(config.monthes[counter], callback_data=cb_msg)
    reply_markup.row(button)
    next_counter = counter + 1
    if next_counter > 11:
        next_counter = 0
    cb_msg = concat_owner_month(next_counter, owner)
    buttonr = InlineKeyboardButton(str(next_counter), callback_data=cb_msg)
    prev_counter = counter - 5
    if prev_counter < 0:
        prev_counter = 9
    cb_msg = concat_owner_month(prev_counter, owner)
    buttonl = InlineKeyboardButton(str(prev_counter), callback_data=cb_msg)
    reply_markup.add(buttonl, buttonr)

    return reply_markup

def concat_owner_month(month, owner):
    result = str(month) + ":" + str(owner)
    return result
