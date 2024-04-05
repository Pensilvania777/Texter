import asyncio
import io
import logging
import sys
import os
import sqlite3
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from PIL import Image, ImageDraw, ImageFont
import random
import string
from utils.state import Captcha
from aiogram.fsm.context import FSMContext
from aiogram.types import InputFile, FSInputFile

from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)


async def start_reff(message: Message, bot: Bot, state: FSMContext):
    try:

        user_id = message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute('SELECT external_id FROM users_shop WHERE external_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        print(result)
        if result:
            ru = "ru"
            en = "en"
            key_language = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Русский 🇷🇺", callback_data=f'laungeuage_start_{ru}')],
                [InlineKeyboardButton(text="English 🇬🇧", callback_data=f'laungeuage_start_{en}')]
            ])
            await bot.send_message(message.chat.id, "Выберите язык\n"
                                                    "Choose language\n",
                                   reply_markup=key_language)

        else:
            print("refka")
            start_command = message.text
            referrer_id = str(start_command[7:])
            print(referrer_id)
            if referrer_id != "":
                try:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Удалить 🗑", callback_data=f'mess_del')]
                    ])

                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        'INSERT INTO refferrss (user_id, reffer_id, col_sale, reff_acative ) VALUES (?, ?, 0, 0)',
                        (user_id, referrer_id))

                    conn.commit()
                    conn.close()

                    ru = "ru"
                    en = "en"
                    print("GAY1")
                    await bot.send_message(referrer_id, "По вашей ссылке зарегистрирован новый пользователь.",
                                           reply_markup=keyboard)
                    key_language = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Русский 🇷🇺", callback_data=f'laungeuage_start_{ru}')],
                        [InlineKeyboardButton(text="English 🇬🇧", callback_data=f'laungeuage_start_{en}')]
                    ])
                    await bot.send_message(message.chat.id, "Выберите язык\n"
                                                            "Choose language\n",
                                           reply_markup=key_language)
                except:
                    await language_start_set(message, bot, state)
                    pass


            else:
                ru = "ru"
                en = "en"
                key_language = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Русский 🇷🇺", callback_data=f'laungeuage_start_{ru}')],
                    [InlineKeyboardButton(text="English 🇬🇧", callback_data=f'laungeuage_start_{en}')]
                ])
                await bot.send_message(message.chat.id, "Выберите язык\n"
                                                        "Choose language\n",
                                       reply_markup=key_language)
        await bot.delete_message(message.chat.id, message.message_id)

    except:
        pass


async def language_start_set(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:

        language = call.data.split('_')[2]

        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users_shop WHERE external_id = ?", (user_id,))
        count = cursor.fetchone()[0]

        # Если запись существует, обновляем значение launge_user
        if count > 0:
            cursor.execute("UPDATE users_shop SET launge_user = ? WHERE external_id = ?", (language, user_id))
        # Если запись не существует, создаем новую запись
        else:
            cursor.execute("INSERT INTO users_shop (external_id, launge_user) VALUES (?, ?)", (user_id, language))

        # Выполняем коммит, чтобы сохранить изменения
        conn.commit()

        print(language)
        await generate_animal_captcha(bot, call.message)
    except:
        pass


import random

async def generate_animal_captcha(bot: Bot, message: Message):
    try:
        animals = ['🐔', '💣', '🎰', '🎲']
        correct_animal = random.choice(animals)
        random.shuffle(animals)
        key_city_buttons = []
        for animal in animals:
            key_city_buttons.append([InlineKeyboardButton(text=animal, callback_data=f'check_animal_{animal}_{correct_animal}')])
        key_city = InlineKeyboardMarkup(inline_keyboard=key_city_buttons)
        await bot.send_message(message.chat.id, f'Выберите животное {correct_animal} :', reply_markup=key_city)
        await bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        print(repr(e))
# Обработчик для нажатия на кнопку
async def on_button_pressed(call: CallbackQuery, bot: Bot):
    try:
        your_animal = call.data.split('_')[2]

        true_animal = call.data.split('_')[3]

        if your_animal == true_animal:
            await get_start(call.message, bot)
        else:
            await generate_animal_captcha(bot, call.message)
    except Exception as e:
        print(repr(e))



async def get_start(message: Message, bot: Bot):
    try:

        name_user = message.from_user.username
        user_id = message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users_shop WHERE external_id = ?", (user_id,))
        existing_user = cursor.fetchone()
        conn.close()
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT launge_user FROM users_shop WHERE external_id = ?", (user_id,))
        laung = cursor.fetchone()
        conn.close()
        print(laung)
        launge = laung[0]
        print(launge[0])
        if existing_user:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_menu, photo_menu FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Покупка 🛍", callback_data=f'buy_ins_{launge}')],
                    [InlineKeyboardButton(text="Мой аккаунт 👨‍🏫", callback_data=f'my_acc_{launge}')],

                    [
                        InlineKeyboardButton(text="Язык 🌍", callback_data=f'language_{launge}'),
                        InlineKeyboardButton(text="Комментарии 📨", callback_data=f'comview_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Правила 📑", callback_data=f'faq_{launge}'),
                        InlineKeyboardButton(text="Инструкция 📋", callback_data=f'instruction_{launge}')
                    ],
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)



            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_menu, photo_menu FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Purchase 🛍", callback_data=f'buy_ins_{launge}')],
                    [InlineKeyboardButton(text="My account 👨‍🏫", callback_data=f'my_acc_{launge}')],
                    [
                        InlineKeyboardButton(text="Language 🌍", callback_data=f'language_{launge}'),
                        InlineKeyboardButton(text="Comment 📨", callback_data=f'comview_{launge}')

                    ],
                    [

                        InlineKeyboardButton(text="Rules 📑", callback_data=f'faq_{launge}'),
                        InlineKeyboardButton(text="Instructions 📋", callback_data=f'instruction_{launge}')

                    ]

                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)

        else:
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users_shop (name_user, external_id) VALUES (?, ?)",
                           (name_user, user_id))
            conn.commit()
            conn.close()

            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_menu, photo_menu FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Покупка 🛍", callback_data=f'buy_ins_{launge}')],
                    [InlineKeyboardButton(text="Мой аккаунт 👨‍🏫", callback_data=f'my_acc_{launge}')],

                    [
                        InlineKeyboardButton(text="Язык 🌍", callback_data=f'language_{launge}'),
                        InlineKeyboardButton(text="Комментарии 📨", callback_data=f'comview_{launge}')
                    ],
                    [
                        InlineKeyboardButton(text="Правила 📑", callback_data=f'faq_{launge}'),
                        InlineKeyboardButton(text="Инструкция 📋", callback_data=f'instruction_{launge}')
                    ],
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)

            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_menu, photo_menu FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Purchase 🛍", callback_data=f'buy_ins_{launge}')],
                    [InlineKeyboardButton(text="My account 👨‍🏫", callback_data=f'my_acc_{launge}')],
                    [
                        InlineKeyboardButton(text="Language 🌍", callback_data=f'language_{launge}'),
                        InlineKeyboardButton(text="Comment 📨", callback_data=f'comview_{launge}')

                    ],
                    [

                        InlineKeyboardButton(text="Rules 📑", callback_data=f'faq_{launge}'),
                        InlineKeyboardButton(text="Instructions 📋", callback_data=f'instruction_{launge}')

                    ]

                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)
            await bot.delete_message(message.chat.id, message.message_id)

    except:
        pass
