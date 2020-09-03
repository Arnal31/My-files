import telebot
import date
import info_filter
import exceptions
import parsedesc
import logging

from Railways_telegramBot import db
from parse import rail_parse
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1178568039:AAFyfE-FN2lx4Rq5ty2-rZuRTkAkjyfk7ZQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# users = (820094907, 474521191)
#
#
# @bot.message_handler(func=lambda message: message.from_user.id not in users)
# def check_user_id(message):
# bot.send_message(message.chat.id, "🔒Извините, вы не можете пользоваться ботом")


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.send_message(msg.from_user.id,
                     f'✅Здраствуйте, <i>{msg.from_user.first_name}</i>,\n'
                     '✅Я бот, который ищет для вас билеты\n'
                     '✅Чтобы начать, введите сообщение в формате: <i>"Путь1" / "Путь2 / Дата"</i>\n\n'
                     '✅<b>Формат даты:</b> <i>день/месяц/год</i>\n'
                     '✅<b>Пример ввода:</b> "<i>Луговой / Нур-султан / 24-02-2020</i>"',
                     parse_mode='HTML')


@bot.message_handler(commands=['desc'])
def send_description(msg):
    bot.send_message(msg.from_user.id, '✅Чтобы искать, введите сообщение в формате <i>"Путь1" / "Путь2 / Дата"</i>\n\n'
                                       '✅<b>Формат даты:</b> <i>день/месяц/год</i>\n'
                                       '✅<b>Пример ввода:</b> "<i>Луговой / Нур-султан / 24-02-2020</i>"',
                     parse_mode='HTML')


# noinspection PyGlobalUndefined
@bot.message_handler(content_types=['text'])
def send_railways(message):
    global info

    # Получение текста от пользователя
    text = message.text.lower().replace(' ', '').split('/')

    # Получить номера городов из бд
    try:
        departure_way = db.select_city_id(text[0])
        arrival_way = db.select_city_id(text[1])
    except IndexError:
        bot.send_message(message.from_user.id, '❌Ошибка❌\nВведите формат правильно.\n'
                                               'Чтобы получить информацию о вводе введите /desc')
        return
    except exceptions.RouteError:
        bot.send_message(message.from_user.id, "❌Ошибка❌\nВведите путь корректно")
        return

    # кодировка даты
    try:
        user_date = date.date_correct(text[2])
    except exceptions.DateError:
        bot.send_message(message.from_user.id, "❌Ошибка❌\nВведите дату корректно")
        return
    except exceptions.DateErrorLast:
        bot.send_message(message.from_user.id, "❌Ошибка❌\nВведенная дата просрочена")
        return

    bot.send_message(message.from_user.id, "🔎<b>Начинаю поиск</b>🔍", parse_mode='HTML')

    # Получить инфо о рейсах
    try:
        info = rail_parse.get_block(departure_way, arrival_way, user_date)
    except exceptions.NoTrainError:
        msg = 'В данную дату поезда не ездят'
        bot.send_message(message.from_user.id, msg)
        return

    # Обработка данных
    for ifs in info.text:
        train_list = info_filter.info_filter(ifs)
        markup = telebot.types.InlineKeyboardMarkup()
        description = 'desc' + ifs.num
        kb = telebot.types.InlineKeyboardButton(text="📰Описания", callback_data=description)
        markup.add(kb)
        bot.send_message(message.from_user.id, train_list, parse_mode="HTML", reply_markup=markup)

    # Количество поездов
    msg = f'<b>Найдено поездов:</b>{len(info.text)}\n'
    bot.send_message(message.from_user.id, msg, parse_mode="HTML")

    # Ссылка
    mark = telebot.types.InlineKeyboardMarkup()
    mark.add(telebot.types.InlineKeyboardButton(text="Ссылка", url=f"{info.url}"))
    bot.send_message(message.from_user.id,
                     "<b>Нажмите кнопку чтобы перейти на сайт:</b>",
                     parse_mode="HTML",
                     reply_markup=mark)


# noinspection PyGlobalUndefined
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global number
    for informations in info.text:
        if call.data == "desc" + informations.num:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Получаю описания')
            inline_mark_up = telebot.types.InlineKeyboardMarkup()
            desc_back = 'desc_back' + informations.num
            kb = telebot.types.InlineKeyboardButton(text="⏪Назад", callback_data=desc_back)
            inline_mark_up.add(kb)
            desc = parsedesc.descparse(informations.num)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=inline_mark_up,
                                  text=desc)

        elif call.data == 'desc_back' + informations.num:
            back = info_filter.info_filter(informations)
            description = 'desc' + informations.num
            back_markup = telebot.types.InlineKeyboardMarkup()
            back_button = telebot.types.InlineKeyboardButton(text="📰Описания", callback_data=description)
            back_markup.add(back_button)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=back,
                                  reply_markup=back_markup,
                                  parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
