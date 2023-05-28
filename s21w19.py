# -*- coding: utf-8 -*-
import telebot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
import re, time
import config, sqlite_bot, bd_next, bd, bd_list
import threading
#temp
import random

bot = telebot.TeleBot(config.token);
bot_id = bot.get_me().id

@bot.message_handler(commands=["ближайшаяднюха", "birthday_next"])
def birthday_next(message):
    output_message = bd_next.output(message.chat.id, message.from_user.id)
    bot.send_message(message.chat.id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def inline_keyboard(call):
    bot.send_message(config.manual_chat_id, call.data, reply_to_message_id=config.manual_thread_id)

@bot.message_handler(commands=["днюхи", "birthday_list"])
def birthday_list(message):
    options = []
    reply_markup = InlineKeyboardMarkup([options])
    for item in config.monthes:
        button = InlineKeyboardButton(item, callback_data=item)
        reply_markup.row(button)

    output_message=bd_list.output(message)
    bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id, reply_markup=reply_markup)

@bot.message_handler(commands=["днюха", "birthday"])
def birthday(message):
    output_message = bd.output(message)
    bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

@bot.message_handler(commands=["помощь"])
def helpmenu(message):
    bot.send_message(message.chat.id, config.help_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

event_job = threading.Event()
def job_handler():
    while not event_job.is_set():
        days_left = bd_next.count_days(config.manual_chat_id, bot_id)
        if days_left < 3:
            output_message = bd_next.output(config.manual_chat_id, bot_id)
            bot.send_message(config.manual_chat_id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")
        event_job.wait(43200)

job_thread = threading.Thread(target=job_handler)
job_thread.start()

bot.polling(none_stop=True, interval=1)

event_job.set()
job_thread.join()
