from telebot import types
import telebot
import config
import reghandler
import dbhandler
import json

# Owner info
owner = config.OWNER

bot = telebot.TeleBot(config.TOKEN, parse_mode=config.PARSE_MODE)

# Commands list and their descriptions
commands = [
    [
        'link',
        'help',
        'register',
        'unregister'
    ],
    [
        'ссылка на платформу',
        'список команд',
        'регистрация в системе отслеживания',
        'отмена регистрации'
    ]
]

# Help message
help_message = ''
for command in commands[0]:
    help_message += ('/' + command + ' - ' +
                     commands[1][commands[0].index(command)] + '\n')
help_message.rstrip('\n')

# Default keyboard buttons
default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
help_button = types.KeyboardButton('Список команд')
link_button = types.KeyboardButton('Платформа')
default_keyboard.add(help_button, link_button)

# Cancel markup inline
cancel_markup_inline = types.InlineKeyboardMarkup(row_width=1)
cancel_button_inline = types.InlineKeyboardButton(
    'Отмена', callback_data='cancel')
cancel_markup_inline.add(cancel_button_inline)


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    sticker = open('../assets/Hello.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(
        message.chat.id, f"Привет, **{message.from_user.first_name}**!\n"
        + "Вот список доступных команд:\n\n"
        + help_message, reply_markup=default_keyboard
    )


@bot.message_handler(commands=['help'])
def help_handler(message: types.Message):
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['link'])
def url_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton(
        'Платформа школы 21', 'https://edu.21-school.ru/')
    markup.add(write_me_button)
    bot.send_message(
        message.chat.id, 'https://edu.21-school.ru/', reply_markup=markup)


@bot.message_handler(commands=['register', 'unregister'])
def registration_handler(message: types.Message):
    if message.text == '/register':
        reghandler.register_user(bot, message)
    elif message.text == '/unregister':
        reghandler.unregister_user(bot, message)


def handle_unknown(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton(
        'Напиши!', 'telegram.me/' + owner)
    markup.add(write_me_button)
    bot.send_message(
        message.chat.id, 'Такой команды я не знаю. Возможно, мой Создатель её ещё не реализовал...\n\n'
        + f'Если хочешь, чтобы Создатель реализовал эту команду, **напиши** ему: @{owner}',
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def text_handler(message: types.Message):
    if message.text == 'Список команд':
        help_handler(message)
    elif message.text == 'Платформа':
        url_handler(message)
    else:
        handle_unknown(message)


bot.infinity_polling()
