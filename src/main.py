from telebot import types
import telebot
import config
import reghandler
import dbhandler

# Owner info
owner = config.OWNER

bot = telebot.TeleBot(config.TOKEN, parse_mode=config.PARSE_MODE)

# Commands list and their descriptions
commands = [
    [
        'link',
        'help',
        'register',
        'unregister',
        'check'
    ],
    [
        'ссылка на платформу',
        'список команд',
        'регистрация в системе отслеживания',
        'отмена регистрации',
        'проверить регистрацию в системе отслеживания'
    ]
]

user_info = []

# Help message
help_message = ''
for command in commands[0]:
    help_message += ('/' + command + ' - ' +
                     commands[1][commands[0].index(command)] + '\n')
help_message.rstrip('\n')

# Default keyboard buttons
default_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard_list = [
    types.KeyboardButton('Список команд'),
    types.KeyboardButton('Платформа')
]
for button in default_keyboard_list:
    default_keyboard_markup.add(button)


@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    sticker = open('../assets/Hello.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(
        message.chat.id, f"Привет, **{message.from_user.first_name}**!\n"
        + "Вот список доступных команд:\n\n"
        + help_message, reply_markup=default_keyboard_markup
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


@bot.message_handler(commands=['register'])
def registration_handler(message: types.Message):
    if not dbhandler.read_from_db(str(message.chat.id)):
        user_info.clear()
        user_info.append('T')
        bot.send_message(message.chat.id, 'Введи свой **логин** на платформе',
                         reply_markup=reghandler.cancel_markup_inline)
    else:
        bot.send_message(message.chat.id, 'Похоже, ты уже зарегистрирован в системе отслеживания оповещений.\nПопробуй выполнить команду /unregister и попробовать ещё раз.\n\n'
                         + f'Если это не помогло, обратись к моему Создателю: @{config.OWNER}')


@bot.message_handler(commands=['unregister'])
def unreg_handler(message: types.Message):
    if dbhandler.read_from_db(str(message.chat.id)):
        dbhandler.remove_from_db(str(message.chat.id))
        bot.send_message(
            message.chat.id, 'Твой никнейм успешно удалён из истемы отслеживания.')
        user_info.clear()
    else:
        bot.send_message(message.chat.id, 'Похоже, ты ещё не зарегистрирован в системе отслеживания оповещений.\n\n'
                         + f'Если это не помогло, обратись к моему Создателю: @{config.OWNER}')


@bot.message_handler(commands=['check'])
def check_registration_handler(message: types.Message):
    if dbhandler.read_from_db(str(message.chat.id)):
        bot.send_message(
            message.chat.id, 'Твой id уже зарегистрирован в системе отслеживания.')
    else:
        bot.send_message(
            message.chat.id, 'Твой id ещё не зарегистрирован в системе отслеживания.')


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
    elif message.text == 'Регистрация':
        registration_handler(message)
    else:
        if len(user_info) != 0:
            if user_info[0] == 'T' and len(user_info) == 1:
                bot.send_message(message.chat.id, 'Теперь введи **пароль** от платформы\n\n__Не бойся, я шифрую данные, так что не смогу их применить__',
                                 reply_markup=reghandler.cancel_markup_inline)
                user_info.append(message.text)
            elif user_info[0] == 'T' and len(user_info) == 2:
                bot.send_message(
                    message.chat.id, f'Ты зарегистрировался под ником **{user_info[1]}**\n\nДля отмены регистрации выполни команду /unregister'
                    + '\n**ОБЯЗАТЕЛЬНО** удали сообщение с паролем в целях конфиденциальности!')
                user_info.append(message.text)
                dbhandler.write_to_db(
                    user_info[1], user_info[2], str(message.chat.id))
                user_info.clear()
            else:
                user_info.clear()
                bot.send_message(
                    message.chat.id, 'Что-то пошло не так. Попробуй ещё раз', reply_markup=None)
        else:
            handle_unknown(message)
            user_info.clear()


@bot.callback_query_handler(func=lambda call: True)
def inline_buttons_handler(call: types.CallbackQuery):
    if call.data == 'cancel':
        bot.edit_message_text(call.message.text + '\n\n__Действие отменено__',
                              call.message.chat.id, call.message.id, reply_markup=None)
        user_info.clear()


bot.infinity_polling()
