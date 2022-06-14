from uuid import NAMESPACE_DNS
import telebot
import dbhandler
import config

# Cancel markup inline
cancel_markup_inline = telebot.types.InlineKeyboardMarkup(row_width=1)
cancel_button_inline = telebot.types.InlineKeyboardButton(
    'Отмена', callback_data='cancel')
cancel_markup_inline.add(cancel_button_inline)


def register_user(bot: telebot.TeleBot, message: telebot.types.Message):
    user_data = message.text.split(' ')
    if len(user_data) != 3:
        bot.send_message(message.chat.id, 'Недостаточно аргументов')
    else:
        dbhandler.write_to_db(
            user_data[1], user_data[2], message.chat.username)
        # Replace later
        bot.send_message(message.chat.id, 'Успешная регистрация!')


def unregister_user(bot: telebot.TeleBot, message: telebot.types.Message):
    if dbhandler.read_from_db(message.chat.username):
        dbhandler.remove_from_db(message.chat.username)
        bot.send_message(
            message.chat.id, 'Твой никнейм успешно удалён из истемы отслеживания.')
    else:
        bot.send_message(message.chat.id, 'Похоже, ты ещё не зарегистрирован в системе отслеживания оповещений.\n\n'
                         + f'Если это ошибка или ты недавно менял свой **id**, обратись к моему создателю: @{config.OWNER}')
