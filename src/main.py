from telebot import types
from telebot import TeleBot
import config
import reghandler as reg
import dbhandler as db
import webhandler as wb
import datetime

# Owner info
owner = config.OWNER

bot = TeleBot(config.TOKEN, parse_mode=config.PARSE_MODE)

# Commands list and their descriptions
commands = [
    ["link", "help", "register", "unregister", "check", "agenda"],
    [
        "ссылка на платформу",
        "список команд",
        "регистрация в системе отслеживания",
        "отмена регистрации",
        "проверить регистрацию в системе отслеживания",
        "получить сводку событий на сегодня",
    ],
]

# Dictionaries to correctly handle user registration
user_info = {}
prev_messages = {}

# Help message
help_message = ""
for command in commands[0]:
    help_message += (
        "/" + command + " - " + commands[1][commands[0].index(command)] + "\n"
    )
help_message.rstrip("\n")

# Default keyboard buttons
default_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_keyboard_list = [
    types.KeyboardButton("Список команд"),
    types.KeyboardButton("Платформа"),
    types.KeyboardButton("Сводка"),
]
for button in default_keyboard_list:
    default_keyboard_markup.add(button)


@bot.message_handler(commands=["start"])
def start_handler(message: types.Message):
    hello_sticker = open("assets/Hello.webp", "rb")
    bot.send_sticker(message.chat.id, hello_sticker)
    hello_sticker.close()
    bot.send_message(
        message.chat.id,
        f"Привет, *{message.from_user.first_name}*!\n"
        + "Вот список доступных команд:\n\n"
        + help_message,
        reply_markup=default_keyboard_markup,
    )


@bot.message_handler(commands=["help"])
def help_handler(message: types.Message):
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=["link"])
def url_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton(
        "Платформа школы 21", "https://edu.21-school.ru/"
    )
    markup.add(write_me_button)
    bot.send_message(message.chat.id, "https://edu.21-school.ru/", reply_markup=markup)


@bot.message_handler(commands=["register"])
def registration_handler(message: types.Message):
    if not db.read_from_db(str(message.chat.id)):
        user_info[str(message.chat.id)] = ["Junk"]
        bot.send_message(
            message.chat.id,
            "Введи свой *логин* на платформе",
            reply_markup=reg.cancel_markup_inline,
        )
    else:
        bot.send_message(
            message.chat.id,
            "Похоже, ты уже зарегистрирован в системе отслеживания оповещений.\nПопробуй выполнить команду /unregister и попробовать ещё раз.\n\n"
            + f"Если это не помогло, обратись к моему Создателю: @{config.OWNER}",
        )


@bot.message_handler(commands=["unregister"])
def unreg_handler(message: types.Message):
    if db.read_from_db(str(message.chat.id)):
        db.remove_from_db(str(message.chat.id))
        bot.send_message(
            message.chat.id, "Твой никнейм успешно удалён из истемы отслеживания."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Похоже, ты ещё не зарегистрирован в системе отслеживания оповещений.\n\n"
            + "Сперва зарегистрируйся, введя команду /register",
        )


@bot.message_handler(commands=["check"])
def check_registration_handler(message: types.Message):
    if db.read_from_db(str(message.chat.id)):
        bot.send_message(
            message.chat.id, "Твой id уже зарегистрирован в системе отслеживания."
        )
    else:
        bot.send_message(
            message.chat.id, "Твой id ещё не зарегистрирован в системе отслеживания."
        )


@bot.message_handler(commands=["agenda"])
def send_agenda(message: types.Message):
    print(f'Checking registration for user id "{message.chat.id}"...')
    user_info = db.read_from_db(str(message.chat.id))
    if not user_info:
        print(f'User with id "{message.chat.id}" is not registered!')
        bot.send_message(
            message.chat.id,
            "Для получения сводки необходимо сперва зарегистрироваться. Ты можешь сделать это с помощью команды /register.",
        )
    else:
        print(f"Found login \"{user_info['login']}\" for id \"{message.chat.id}\"!")
        print(f"Collecting info for user \"{user_info['login']}\"...")
        print("- Authorization...")
        messg = bot.send_message(
            message.chat.id, "*Собираю информацию...*\n\n" + "_[1/2] - авторизация_"
        )
        d = datetime.datetime.today()
        d = d.strftime("%d.%m.%y")
        events = wb.get_today_events(user_info["login"], user_info["password"])
        if events is None:
            print("- Authorization failed!")
            print(f"Failed to authorize user \"{user_info['login']}\"!")
            bot.edit_message_text(
                "Возникли проблемы с авторизацией. Попробуй позже.\n\n"
                + f"_Если не получится позже, напиши Создателю: @{config.OWNER}_",
                message.chat.id,
                messg.id,
            )
        else:
            print("- Authorization success!")
            print(f"Collecting info for username \"{user_info['login']}\"...")
            bot.edit_message_text(
                "*Собираю информацию...*\n\n" + "_[2/2] - получение данных_",
                message.chat.id,
                messg.id,
            )
            if events == []:
                msg = (
                    f"*{d}*\n\n" + "На сегодня у тебя не запланировано никаких событий."
                )
            else:
                msg = f"*{d}*\n\n" + "На сегодня у тебя следующие события:\n"
                for event in events:
                    msg += f"• *{event['start_time']}* - *{event['end_time']}* — _{event['event']}_\n"
                msg.strip("\n")
            print(f"Ended collecting info for username \"{user_info['login']}\".")
            bot.edit_message_text(msg, messg.chat.id, messg.id)


def handle_unknown(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton("Напиши!", "telegram.me/" + owner)
    markup.add(write_me_button)
    bot.send_message(
        message.chat.id,
        "Такой команды я не знаю. Возможно, мой Создатель её ещё не реализовал...\n\n"
        + f"Если хочешь, чтобы Создатель реализовал эту команду, *напиши* ему: @{owner}",
        reply_markup=markup,
    )


def check_help_text(message: types.Message):
    if message.text == "Список команд":
        return True


@bot.message_handler(content_types=["text"], func=check_help_text)
def reg_text_handler(message: types.Message):
    help_handler(message)


def check_platform_text(message: types.Message):
    if message.text == "Платформа":
        return True


@bot.message_handler(content_types=["text"], func=check_platform_text)
def platform_text_handler(message: types.Message):
    url_handler(message)


def check_reg_text(message: types.Message):
    if message.text == "Регистрация":
        return True


@bot.message_handler(content_types=["text"], func=check_reg_text)
def reg_text_handler(message: types.Message):
    registration_handler(message)


def check_agenda_text(message: types.Message):
    if message.text == "Сводка":
        return True


@bot.message_handler(content_types=["text"], func=check_agenda_text)
def agenda_text_handler(message: types.Message):
    send_agenda(message)


@bot.message_handler(content_types=["text"])
def text_handler(message: types.Message):
    if user_info.get(str(message.chat.id), None) is not None:
        if len(user_info.get(str(message.chat.id))) == 1:
            user_info.get(str(message.chat.id)).append(message.text.strip().lower())
            bot.send_message(
                message.chat.id,
                "Теперь введи *пароль* от платформы\n\n_Не бойся, я шифрую данные, так что не смогу их применить_",
                reply_markup=reg.cancel_markup_inline,
            )
        elif len(user_info.get(str(message.chat.id))) == 2:
            tmp_message = bot.send_message(
                message.chat.id, "Проверяю корректность данных..."
            )
            user_info.get(str(message.chat.id)).append(message.text)
            if wb.auth_into_platform(
                username=user_info.get(str(message.chat.id))[1],
                password=user_info.get(str(message.chat.id))[2],
            ):
                db.write_to_db(
                    user_info.get(str(message.chat.id))[1],
                    user_info.get(str(message.chat.id))[2],
                    (str(message.chat.id)),
                )
                bot.edit_message_text(
                    f"Ты зарегистрировался под ником *{user_info.get(str(message.chat.id))[1]}*\n\nДля отмены регистрации выполни команду /unregister"
                    + "\n*ОБЯЗАТЕЛЬНО* удали сообщение с паролем в целях конфиденциальности!",
                    message.chat.id,
                    tmp_message.id,
                )
                user_info.pop(str(message.chat.id), [])
            else:
                bot.edit_message_text(
                    "Мне не удалось авторизоваться на платформе с этими данными. Попробуй ещё раз.",
                    message.chat.id,
                    tmp_message.id,
                )
        else:
            user_info.pop(str(message.chat.id), [])
            bot.send_message(
                message.chat.id,
                "Что-то пошло не так. Попробуй ещё раз",
                reply_markup=None,
            )
    else:
        handle_unknown(message)


@bot.callback_query_handler(func=lambda call: True)
def inline_buttons_handler(call: types.CallbackQuery):
    if call.data == "cancel":
        bot.edit_message_text(
            call.message.text + "\n\n_Действие отменено_",
            call.message.chat.id,
            call.message.id,
            reply_markup=None,
        )
        user_info.pop(call.message.chat.id)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
