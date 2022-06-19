import telebot
import dbhandler
import config

# Cancel markup inline
cancel_markup_inline = telebot.types.InlineKeyboardMarkup(row_width=1)
cancel_button_inline = telebot.types.InlineKeyboardButton(
    "Отмена", callback_data="cancel"
)
cancel_markup_inline.add(cancel_button_inline)


def unregister_user(bot: telebot.TeleBot, message: telebot.types.Message):
    if dbhandler.read_from_db(str(message.chat.id)):
        dbhandler.remove_from_db(str(message.chat.id))
        bot.send_message(
            message.chat.id, "Твой никнейм успешно удалён из истемы отслеживания."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Похоже, ты ещё не зарегистрирован в системе отслеживания оповещений.\n\n"
            + f"Если это не помогло, обратись к моему Создателю: @{config.OWNER}",
        )
