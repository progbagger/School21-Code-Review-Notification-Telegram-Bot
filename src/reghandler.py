import telebot

# Cancel markup inline
cancel_markup_inline = telebot.types.InlineKeyboardMarkup(row_width=1)
cancel_button_inline = telebot.types.InlineKeyboardButton(
    'Отмена', callback_data='cancel')
cancel_markup_inline.add(cancel_button_inline)


def register_user(bot: telebot.TeleBot, message: telebot.types.Message):
    # Placeholder message for now
    bot.send_message(
        message.chat.id, 'Ты захотел **зарегистрироваться**, но...\n'
        + 'Данная функция ещё в разработке, '
        + 'Создатель скоро воплотит её в реальность...',
        reply_markup=cancel_markup_inline
    )


def unregister_user(bot: telebot.TeleBot, message: telebot.types.Message):
    # Placeholder message for now
    bot.send_message(
        message.chat.id, 'Ты захотел **отменить регистрацию**, но...\n'
        + 'Данная функция ещё в разработке, '
        + 'Создатель скоро воплотит её в реальность...',
        reply_markup=cancel_markup_inline
    )
