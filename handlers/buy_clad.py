from aiogram import Bot
from aiogram.types import (Message,
                           InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
import sqlite3
from datetime import datetime
import traceback
from urllib.parse import urlencode, unquote


async def buy_clad(call: CallbackQuery, bot: Bot):
    try:

        launge = call.data.split('_')[2]
        user_id = call.message.chat.id
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM city")
        cities = cursor.fetchall()
        conn.close()
        if len(cities) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_city, photo_city FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)

            elif launge == "ua":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, "Виберіть місто:", reply_markup=keyboard)
            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_city, photo_city FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Back 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_photo(user_id, photo_menu, caption=text_menu, reply_markup=keyboard)
            elif launge == "pl":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text=city[1], callback_data=f'_ars_city_{city[1]}_{launge}')
                        for city in cities
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'back_menu_st_{launge}')
                    ]
                ])
                await bot.send_message(call.message.chat.id, "Wybierz miasto:", reply_markup=keyboard)

            # Отправляем сообщение с инлайновыми кнопками
            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data='back_menu_st_')
                ]
            ])
            await bot.send_message(call.message.chat.id, f"Нет Города.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))

async def buy_item(call: CallbackQuery, bot: Bot):
    try:

        city = call.data.split('_')[3]
        launge = call.data.split('_')[4]

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name_item FROM clad WHERE name_city = ?", (city,))
        unique_items = cursor.fetchall()
        conn.close()

        if len(unique_items) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_item, photo_item FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(unique_items), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(unique_items) - 1:
                        row.append(InlineKeyboardButton(text=unique_items[i][0], callback_data=f'_ars_item_{city}_{unique_items[i][0]}_{launge}'))
                        row.append(
                            InlineKeyboardButton(text=unique_items[i + 1][0], callback_data=f'_ars_item_{city}_{unique_items[i + 1][0]}_{launge}'))
                    else:
                        row.append(InlineKeyboardButton(text=unique_items[i][0], callback_data=f'_ars_item_{city}_{unique_items[i][0]}_{launge}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'buy_clad_{launge}')
                ])
                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=key_city)

            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_item, photo_item FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(unique_items), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(unique_items) - 1:
                        row.append(InlineKeyboardButton(text=unique_items[i][0],
                                                        callback_data=f'_ars_item_{city}_{unique_items[i][0]}_{launge}'))
                        row.append(
                            InlineKeyboardButton(text=unique_items[i + 1][0],
                                                 callback_data=f'_ars_item_{city}_{unique_items[i + 1][0]}_{launge}'))
                    else:
                        row.append(InlineKeyboardButton(text=unique_items[i][0],
                                                        callback_data=f'_ars_item_{city}_{unique_items[i][0]}_{launge}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Back 🔙", callback_data=f'buy_clad_{launge}')
                ])

                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=key_city)

            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'buy_clad_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                ]
            ])
            await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                         f"Товар не найден.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def buy_area(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        launge = call.data.split('_')[5]
        item = call.data.split('_')[4]
        print(city,item, launge)
        count = 0
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name_area FROM clad WHERE name_city = ? AND name_item = ?", (city, item))
        arks = cursor.fetchall()
        cursor.execute("SELECT name_gram, COUNT(*) FROM clad WHERE name_city = ? AND name_item = ?  GROUP BY name_gram", (city, item))
        areas = cursor.fetchall()
        conn.close()

        for area in areas:
            gram, count = area
        if len(areas) > 0:
            if launge == "ru":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_area, photo_area FROM oform_ru WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                print(arks)
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(arks), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(arks) - 1:
                        row.append(InlineKeyboardButton(text=f"{arks[i][0]} - ({count} шт.) ",
                                                        callback_data=f'_ars_area_{city}_{arks[i][0]}_{launge}_{item}'))
                        row.append(
                            InlineKeyboardButton(text=f"{arks[i + 1][0]} - ({count} шт.) ",
                                                 callback_data=f'_ars_area_{city}_{arks[i + 1][0]}_{launge}_{item}'))
                    else:
                        row.append(InlineKeyboardButton(text=f"{arks[i][0]} - ({count} шт.) ",
                                                        callback_data=f'_ars_area_{city}_{arks[i][0]}_{launge}_{item}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}')
                ])
                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=key_city)

            elif launge == "en":
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute('''SELECT text_area, photo_area FROM oform_en WHERE id = ?''', (1,))

                result = cursor.fetchone()
                text_menu = ""
                photo_menu = ""
                if result:
                    text_menu, photo_menu = result
                conn.close()
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(arks), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(arks) - 1:
                        row.append(InlineKeyboardButton(text=f"{arks[i][0]} - ({count} am.) ",
                                                        callback_data=f'_ars_area_{city}_{arks[i][0]}_{launge}_{item}'))
                        row.append(
                            InlineKeyboardButton(text=f"{arks[i + 1][0]} - ({count} am.) ",
                                                 callback_data=f'_ars_area_{city}_{arks[i + 1][0]}_{launge}_{item}'))
                    else:
                        row.append(InlineKeyboardButton(text=f"{arks[i][0]} - ({count} am.) ",
                                                        callback_data=f'_ars_area_{city}_{arks[i][0]}_{launge}_{item}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_city_{city}_{launge}')
                ])

                await bot.send_photo(call.message.chat.id, photo_menu, caption=text_menu, reply_markup=key_city)

            await bot.delete_message(call.message.chat.id, call.message.message_id)

        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f" В городе {city} нет районов.", reply_markup=keyboard)

            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_city_{city}_{launge}'),
                        InlineKeyboardButton(text="Меню 💫", callback_data=f'back_menu_st_{launge}')
                    ],

                ])
                await bot.send_message(call.message.chat.id, f"There are no districts in {city}.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(repr(e))


async def buy_gram(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        item = call.data.split('_')[6]
        launge = call.data.split('_')[5]
        print(city, area, item ,launge)

        itemsnow = item

        print(city, area, item)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM item WHERE name_item = ?", (item,))
        items = cursor.fetchall()
        conn.close()
        if len(items) > 0:
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name_gram FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? GROUP BY name_gram",
                           (city, area, itemsnow))
            grams = cursor.fetchall()
            conn.close()
            print(grams)
            name_item = ""
            caption_item = ""
            price_item = ""
            for item in items:
                name_item = item[1]
                caption_item = item[2]
                price_item = item[3]
            photo_data = item[4]
            unique_grams = ""
            for gram in grams:
                unique_grams = gram[0]
                print(gram[0])
            print(unique_grams)

            if launge == "ru":
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(grams), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(grams) - 1:
                        row.append(InlineKeyboardButton(text=grams[i][0],
                                                        callback_data=f'_ars_gram_{city}_{area}_{grams[i][0]}_{launge}_{itemsnow}'))
                        row.append(
                            InlineKeyboardButton(text=grams[i + 1][0],
                                                 callback_data=f'_ars_gram_{city}_{area}_{grams[i + 1][0]}_{launge}_{itemsnow}'))
                    else:
                        row.append(InlineKeyboardButton(text=grams[i][0],
                                                        callback_data=f'_ars_gram_{city}_{area}_{grams[i][0]}_{launge}_{itemsnow}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                ])

                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {name_item}\n"
                                                                               f"Описание: {caption_item}\n"
                                                                               f"Цена за грамм : {price_item} $\n"
                                                                               f"Выберите граммовку:",
                                     reply_markup=key_city)


            elif launge == "en":
                key_city = InlineKeyboardMarkup(inline_keyboard=[])

                for i in range(0, len(grams), 2):
                    row = []
                    # Добавляем две кнопки в строку, если есть два города
                    if i < len(grams) - 1:
                        row.append(InlineKeyboardButton(text=f"{grams[i][0]} ",
                                                        callback_data=f'_ars_gram_{city}_{area}_{grams[i][0]}_{launge}_{itemsnow}'))
                        row.append(
                            InlineKeyboardButton(text=grams[i + 1][0],
                                                 callback_data=f'_ars_gram_{city}_{area}_{grams[i + 1][0]}_{launge}_{itemsnow}'))
                    else:
                        row.append(InlineKeyboardButton(text=f"{grams[i][0]}",
                                                        callback_data=f'_ars_gram_{city}_{area}_{grams[i][0]}_{launge}_{itemsnow}'))
                    key_city.inline_keyboard.append(row)

                key_city.inline_keyboard.append([
                    InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                ])
                await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                               f"Description: {caption_item}\n"
                                                                               f"Price per gram: {price_item} $\n"
                                                                               f"Select grammar:",
                                     reply_markup=key_city)



            await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_item_{city}_{itemsnow}_{launge}')
                ],
                [
                    InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                ]

            ])

            await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                         f"Район({area})\n"
                                                         f"Товар не найден.", reply_markup=keyboard)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)


async def buy_item_end(call: CallbackQuery, bot: Bot):
    try:
        user_id = call.message.chat.id
        city = call.data.split('_')[3]
        area = call.data.split('_')[4]
        gram = call.data.split('_')[5]
        launge = call.data.split('_')[6]
        item = call.data.split('_')[7]

        print(city,area,item,gram,launge)
        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price_item, latitude, longtitude FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? AND name_gram = ?",
            (city, area, item, gram))

        result = cursor.fetchone()
        conn.close()
        if result:
            price_item, latitude, longtitude = result
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM item WHERE name_item = ?", (item,))
            rare = cursor.fetchone()
            conn.close()
            print(price_item, latitude, longtitude, rare)

            if rare:

                name_item = rare[1]
                caption_item = rare[2]
                price = rare[3]
                photo_data = rare[4]
                print(name_item, caption_item, price, photo_data)
                conn = sqlite3.connect('shop.db')
                cursor = conn.cursor()
                cursor.execute("SELECT col_sale FROM refferrss WHERE user_id = ?", (user_id,))
                result = cursor.fetchone()
                conn.close()
                print(price_item)
                discount_amount = 0.10 * int(price_item)
                print(area)
                area = area.replace(" ", "+")
                if result is None:
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {item}\n"
                                                                                       f"Цена за грамм: {price} $\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} $\n",
                                             reply_markup=keyboard)

                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {item}\n"
                                                                                       f"Price per gram: {price} $\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} $\n",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif result[0] > 0:
                    print(discount_amount)
                    price_item_sale = price_item - discount_amount
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {item}\n"
                                                                                       f"Цена за грамм: {price} $\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} $\n",
                                             reply_markup=keyboard)


                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item_sale}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {item}\n"
                                                                                       f"Price per gram: {price} $\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} $\n",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                else:
                    if launge == "ru":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Купить ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Отменить ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Товар: {item}\n"
                                                                                       f"Цена за грамм: {price} $\n"
                                                                                       f"Граммовка: {gram} грамм\n"
                                                                                       f"Цена: {price_item} $\n",
                                             reply_markup=keyboard)

                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Buy ✅",
                                                     callback_data=f'_ars_end_{city}_{area}_{item}_{gram}_{price_item}_{launge}')
                            ] +
                            [
                                InlineKeyboardButton(text="Cancel ❌", callback_data=f'back_menu_st_{city}_{area}_{item}')
                            ],
                            [
                                InlineKeyboardButton(text="Back 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_data, caption=f"Product: {name_item}\n"
                                                                                       f"Price per gram: {price} $\n"
                                                                                       f"Gram: {gram} gram\n"
                                                                                       f"Price: {price_item} $\n",
                                             reply_markup=keyboard)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)


            else:
                if launge == "ru":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                                 f"Район({area})\n"
                                                                 f"Товар не найден.", reply_markup=keyboard)

                elif launge == "en":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                        ],
                        [
                            InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                        ]
                    ])

                    await bot.send_message(call.message.chat.id, f"City({city})\n"
                                                                 f"Area({area})\n"
                                                                 f"Product not found.", reply_markup=keyboard)

        else:
            if launge == "ru":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"Город({city})\n"
                                                             f"Район({area})\n"
                                                             f"Товар не найден.", reply_markup=keyboard)


            elif launge == "en":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                    ],
                    [
                        InlineKeyboardButton(text="Назад 🔙", callback_data=f'_ars_area_{city}_{area}_{launge}_{item}')
                    ]
                ])

                await bot.send_message(call.message.chat.id, f"City({city})\n"
                                                             f"Area({area})\n"
                                                             f"Product not found.", reply_markup=keyboard)


    except Exception as e:
        traceback.print_exc()


async def buy_end_ars(call: CallbackQuery, bot: Bot):
    try:
        city = call.data.split('_')[3]
        area = call.data.split('_')[4].replace("+", " ")
        item = call.data.split('_')[5]
        gram = call.data.split('_')[6]
        price_item = call.data.split('_')[7]
        price_item_summ = int(price_item)
        launge = call.data.split('_')[8]
        print(area)
        print(area)
        external_id = call.message.chat.id

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users_shop WHERE external_id = ?", (external_id,))
        bal = cursor.fetchone()
        conn.close()
        keyboard_cancel = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
            ]
        ])
        balance = 0
        if bal:
            balance = int(bal[0])
        print(balance, price_item_summ)
        if balance > price_item_summ:
            balance_value = balance
            print(balance_value)
            conn = sqlite3.connect('shop.db')
            cursor = conn.cursor()
            print(city,area,item,gram)
            cursor.execute(
                "SELECT id, price_item, latitude, longtitude, photo_clad FROM clad WHERE name_city = ? AND name_area = ? AND name_item = ? AND name_gram = ?",
                (city, area, item, gram))

            result = cursor.fetchone()
            conn.close()
            if result:
                id_item, price_item, latitude, longtitude, photo_clad = result
                balance_final = int(balance_value)
                price_final = int(price_item_summ)
                print(price_final)
                if balance_final >= price_final:
                    summ_balance = balance_final - int(price_item_summ)
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users_shop SET balance = ? WHERE external_id = ?", (summ_balance, external_id))
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO active_clad ( external_id ,name_city, name_area, name_item, name_gram, price_item, latitude, longtitude, photo_clad)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        external_id, city, area, item, gram, price_item, latitude, longtitude, photo_clad))
                    conn.commit()
                    conn.close()

                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM clad WHERE id = ?", (id_item,))
                    conn.commit()
                    conn.close()

                    print(summ_balance)

                    current_datetime = datetime.now()

                    purchase_day = current_datetime.day
                    purchase_month = current_datetime.month
                    conn = sqlite3.connect('shop.db')
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO analist (city, item, col, price, day, mont) VALUES (?, ?, ?, ?, ?, ?)",
                                   (city, item, gram, price_item, purchase_day,
                                    purchase_month))
                    conn.commit()
                    conn.close()
                    print("DAUN 2")
                    print(launge)
                    if launge == "ru":
                        print("DAUN 3")
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Локация 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Товар: {item}\n"
                                                                                       f"Граммовка: {gram}\n"
                                                                                       f"Цена: {price_item}\n"
                                                                                       f"Широта: {latitude}\n"
                                                                                       f"Долгота: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "ua":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Локація 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Меню 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Товар: {item}\n"
                                                                                       f"Грамування: {gram}\n"
                                                                                       f"Ціна: {price_item}\n"
                                                                                       f"Широта: {latitude}\n"
                                                                                       f"Довгота: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "en":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Location 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Product: {item}\n"
                                                                                       f"Gram: {gram}\n"
                                                                                       f"Price: {price_item}\n"
                                                                                       f"Latitude: {latitude}\n"
                                                                                       f"Longitude: {longtitude}",
                                             reply_markup=keyboard)

                    elif launge == "pl":
                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Lokalizacja 📍",
                                                     callback_data=f'_loc_clad_{latitude}_{longtitude}_{launge}')
                            ],

                            [
                                InlineKeyboardButton(text="Menu 💫", callback_data='back_menu_st_')
                            ]
                        ])

                        await bot.send_photo(call.message.chat.id, photo_clad, caption=f"Produkt: {item}\n"
                                                                                       f"Gram: {gram}\n"
                                                                                       f"Cena: {price_item}\n"
                                                                                       f"Szerokość geograficzna: {latitude}\n"
                                                                                       f"Długość geograficzna: {longtitude}",
                                             reply_markup=keyboard)

                    await bot.delete_message(call.message.chat.id, call.message.message_id)
                else:
                    if launge == "ru":
                        await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "ua":
                        await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "en":
                        await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

                    elif launge == "pl":
                        await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                               reply_markup=keyboard_cancel)
                        await bot.delete_message(call.message.chat.id, call.message.message_id)

            else:
                if launge == "ru":
                    await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "ua":
                    await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "en":
                    await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)

                elif launge == "pl":
                    await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                           reply_markup=keyboard_cancel)
                    await bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            if launge == "ru":
                await bot.send_message(call.message.chat.id, "Ваш баланс недостаточный:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "ua":
                await bot.send_message(call.message.chat.id, "Ваш баланс недостатній:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "en":
                await bot.send_message(call.message.chat.id, "Your balance is insufficient:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)

            elif launge == "pl":
                await bot.send_message(call.message.chat.id, "Twoje saldo jest niewystarczające:",
                                       reply_markup=keyboard_cancel)
                await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")