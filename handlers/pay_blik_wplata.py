from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
import re
from utils.state import Rass, City, Admin, Area, Item, Gram, Balance, Balance_del, Clad
import logging
from utils.state import oform_ru
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

async def pay_blik_wplata(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        language = call.data.split('_')[2]
        print(language)
        if language == 'ru':
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_blick_wplata, photo_blick_wplata FROM oform_ru WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data=f'bliker_{language}'),
                ]

            ])
            await bot.send_photo(call.message.chat.id, photo_menu,
                                 caption=text_menu, reply_markup=keyboard)
        elif language == "en":
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT text_blick_wplata, photo_blick_wplata FROM oform_en WHERE id = ?''', (1,))

            result = cursor.fetchone()
            text_menu = ""
            photo_menu = ""
            if result:
                text_menu, photo_menu = result
            conn.close()
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Back", callback_data=f'bliker_{language}'),
                ]

            ])
            await bot.send_photo(call.message.chat.id, photo_menu,
                                 caption=text_menu, reply_markup=keyboard)
        await bot.delete_message(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(e)