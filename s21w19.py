# -*- coding: utf-8 -*-
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
import re, time, datetime
import config, sqlite_bot, bd_next, bd, bd_list
import threading
#temp
import random

bot = AsyncTeleBot(config.token);
# bot_id = bot.get_me().id

@bot.message_handler(commands=["ближайшаяднюха", "birthday_next"])
async def birthday_next(message):
    output_message = bd_next.output(message.chat.id, message.from_user.id)
    await bot.send_message(message.chat.id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
async def inline_keyboard(call):
    get_num_month = [n for n, x in enumerate(config.monthes) if call.data in x]
    output_message = bd_list.month_list(get_num_month, bot_id)
    await bot.send_message(config.manual_chat_id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")

@bot.message_handler(commands=["днюхи", "birthday_list"])
async def birthday_list(message):
    options = []
    reply_markup = InlineKeyboardMarkup([options])
    for item in config.monthes:
        button = InlineKeyboardButton(item, callback_data=item)
        reply_markup.row(button)

    output_message=bd_list.output(message)
    await bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id, reply_markup=reply_markup)

@bot.message_handler(commands=["днюха", "birthday"])
async def birthday(message):
    output_message = bd.output(message)
    await bot.send_message(message.chat.id, output_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

@bot.message_handler(commands=["помощь"])
async def helpmenu(message):
    await bot.send_message(message.chat.id, config.help_message, parse_mode="HTML", reply_to_message_id=config.manual_thread_id)

async def job_handler():
    while (1):
        days_left = bd_next.count_days(config.manual_chat_id, bot_id)
        if days_left < 3:
            output_message = bd_next.output(config.manual_chat_id, bot_id)
            await bot.send_message(config.manual_chat_id, output_message, reply_to_message_id=config.manual_thread_id, parse_mode="HTML")
        await asyncio.sleep(43200)

async def starter():
    global bot_id
    bot_id = (await bot.get_me()).id
    task1 = asyncio.create_task(job_handler())
    task2 = asyncio.create_task(bot.polling())

    await task1
    await task2

asyncio.run(starter())
