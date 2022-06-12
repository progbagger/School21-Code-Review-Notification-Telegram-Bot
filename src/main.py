from telebot import types
import telebot

owner_id = '@astadasta'

token = r'5598590455:AAE7KWLxOymGYoN0panqe07fMsloByWtuus'

bot = telebot.TeleBot(token, parse_mode='markdown')

# Ссылка на сайт школы 21
edu_url = r'https://edu.21-school.ru/'

# Сообщение списка комманд
help_message = '/register - регистрация в системе отслеживания\n'
help_message += '/unregister - отмена регистрации в системе отслеживания\n'
help_message += '/help - вызов этого сообщения\n'
help_message += '/edu - Ссылка на сайт личного кабинета школы 21'

# Стандартные кнопки
register = types.KeyboardButton('Регистрация')
help_message_button = types.KeyboardButton('Список комманд')

default_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_markup.add(register, help_message_button)


@bot.message_handler(commands=['edu'])
def platform(message):
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton('School 21', edu_url)
    markup.add(url_button)
    bot.send_message(message.chat.id, edu_url, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    start_message = f'*Привет, {message.from_user.first_name}!*\n\n'
    start_message += 'Чтобы зарегистрироваться в системе, напиши /register.\n'
    start_message += 'Если хочешь посмотреть список всех комманд - введи /help.'

    bot.send_message(message.chat.id, start_message,
                     reply_markup=default_markup)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, help_message,
                     reply_markup=default_markup)


@bot.message_handler(commands=['register'])
def register(message):
    bot.send_message(message.chat.id, 'В разработке...',
                     reply_markup=default_markup)


@bot.message_handler(commands=['unregister'])
def unregister(message):
    markup_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button_keyboard, no_button_keyboard = types.KeyboardButton(
        'Да'), types.KeyboardButton('Нет')
    markup_keyboard.add(yes_button_keyboard, no_button_keyboard)
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    yes_button_inline = types.InlineKeyboardButton(
        'Да', callback_data='continue_unregister')
    no_button_inline = types.InlineKeyboardButton(
        'Нет', callback_data='cancel_unregister')
    markup_inline.add(yes_button_inline, no_button_inline)
    bot.send_message(message.chat.id, '*Вы уверены?*',
                     reply_markup=markup_inline)


@bot.message_handler(content_types=['text'])
def redirect_text_to_commands(message):
    if message.text == 'Список комманд':
        help_command(message)
    elif message.text == 'Регистрация':
        register(message)
    else:
        bot.send_message(
            message.chat.id, f"Я не знаю такой команды.\n\nЕсли хочешь предложить функцию - напиши этому человеку: {owner_id}")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'continue_unregister':
            new_msg = 'Ты нажал "Да", но функция ещё в разработке...'
        elif call.data == 'cancel_unregister':
            new_msg = 'Ты нажал "Нет", но функция ещё в разработке...'

        # Удаляем кнопки
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_msg, reply_markup=None)


bot.infinity_polling()
