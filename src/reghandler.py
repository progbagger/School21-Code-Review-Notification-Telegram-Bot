import telebot


def register_user(bot: telebot.TeleBot, message: telebot.types.Message):
    # Placeholder message for now
    bot.send_message(
        message.chat.id, 'Ты захотел **зарегистрироваться**, но...\n'
        + 'Данная функция ещё в разработке, '
        + 'Создатель скоро воплотит её в реальность...'
    )


def unregister_user(bot: telebot.TeleBot, message: telebot.types.Message):
    # Placeholder message for now
    bot.send_message(
        message.chat.id, 'Ты захотел **отменить регистрацию**, но...\n'
        + 'Данная функция ещё в разработке, '
        + 'Создатель скоро воплотит её в реальность...'
    )
