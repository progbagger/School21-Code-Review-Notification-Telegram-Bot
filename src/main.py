from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
import reghandler as reg
import dbhandler as db

# Owner info
owner = config.OWNER

bot = AsyncTeleBot(config.TOKEN, parse_mode=config.PARSE_MODE)

# Commands list and their descriptions
commands = [
    ["link", "help", "register", "unregister", "check"],
    [
        "ссылка на платформу",
        "список команд",
        "регистрация в системе отслеживания",
        "отмена регистрации",
        "проверить регистрацию в системе отслеживания",
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
]
for button in default_keyboard_list:
    default_keyboard_markup.add(button)


@bot.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    sticker = open("../assets/Hello.webp", "rb")
    await bot.send_sticker(message.chat.id, sticker)
    await bot.send_message(
        message.chat.id,
        f"Привет, **{message.from_user.first_name}**!\n"
        + "Вот список доступных команд:\n\n"
        + help_message,
        reply_markup=default_keyboard_markup,
    )


@bot.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    await bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=["link"])
async def url_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton(
        "Платформа школы 21", "https://edu.21-school.ru/"
    )
    markup.add(write_me_button)
    await bot.send_message(
        message.chat.id, "https://edu.21-school.ru/", reply_markup=markup
    )


@bot.message_handler(commands=["register"])
async def registration_handler(message: types.Message):
    if not db.read_from_db(str(message.chat.id)):
        user_info[str(message.chat.id)] = ["Junk"]
        await bot.send_message(
            message.chat.id,
            "Введи свой **логин** на платформе",
            reply_markup=reg.cancel_markup_inline,
        )
    else:
        await bot.send_message(
            message.chat.id,
            "Похоже, ты уже зарегистрирован в системе отслеживания оповещений.\nПопробуй выполнить команду /unregister и попробовать ещё раз.\n\n"
            + f"Если это не помогло, обратись к моему Создателю: @{config.OWNER}",
        )


@bot.message_handler(commands=["unregister"])
async def unreg_handler(message: types.Message):
    if db.read_from_db(str(message.chat.id)):
        db.remove_from_db(str(message.chat.id))
        await bot.send_message(
            message.chat.id, "Твой никнейм успешно удалён из истемы отслеживания."
        )
    else:
        await bot.send_message(
            message.chat.id,
            "Похоже, ты ещё не зарегистрирован в системе отслеживания оповещений.\n\n"
            + f"Сперва зарегистрируйся, введя команду /register",
        )


@bot.message_handler(commands=["check"])
async def check_registration_handler(message: types.Message):
    if db.read_from_db(str(message.chat.id)):
        await bot.send_message(
            message.chat.id, "Твой id уже зарегистрирован в системе отслеживания."
        )
    else:
        await bot.send_message(
            message.chat.id, "Твой id ещё не зарегистрирован в системе отслеживания."
        )


async def handle_unknown(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton("Напиши!", "telegram.me/" + owner)
    markup.add(write_me_button)
    await bot.send_message(
        message.chat.id,
        "Такой команды я не знаю. Возможно, мой Создатель её ещё не реализовал...\n\n"
        + f"Если хочешь, чтобы Создатель реализовал эту команду, **напиши** ему: @{owner}",
        reply_markup=markup,
    )


def check_help_text(message: types.Message):
    if message.text == "Список команд":
        return True


@bot.message_handler(content_types=["text"], func=check_help_text)
async def reg_text_handler(message: types.Message):
    await help_handler(message)


def check_platform_text(message: types.Message):
    if message.text == "Платформа":
        return True


@bot.message_handler(content_types=["text"], func=check_platform_text)
async def platform_text_handler(message: types.Message):
    await url_handler(message)


def check_reg_text(message: types.Message):
    if message.text == "Регистрация":
        return True


@bot.message_handler(content_types=["text"], func=check_reg_text)
async def reg_text_handler(message: types.Message):
    await registration_handler(message)


@bot.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
    if user_info.get(str(message.chat.id), None) is not None:
        if len(user_info.get(str(message.chat.id))) == 1:
            user_info.get(str(message.chat.id)).append(message.text)
            await bot.send_message(
                message.chat.id,
                "Теперь введи **пароль** от платформы\n\n__Не бойся, я шифрую данные, так что не смогу их применить__",
                reply_markup=reg.cancel_markup_inline,
            )
        elif len(user_info.get(str(message.chat.id))) == 2:
            user_info.get(str(message.chat.id)).append(message.text)
            db.write_to_db(
                user_info.get(str(message.chat.id))[1],
                user_info.get(str(message.chat.id))[1],
                (str(message.chat.id)),
            )
            await bot.send_message(
                message.chat.id,
                f"Ты зарегистрировался под ником **{user_info.get(str(message.chat.id))[1]}**\n\nДля отмены регистрации выполни команду /unregister"
                + "\n**ОБЯЗАТЕЛЬНО** удали сообщение с паролем в целях конфиденциальности!",
            )
            user_info.pop(str(message.chat.id), [])
        else:
            user_info.pop(str(message.chat.id), [])
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так. Попробуй ещё раз",
                reply_markup=None,
            )
    else:
        await handle_unknown(message)


@bot.callback_query_handler(func=lambda call: True)
async def inline_buttons_handler(call: types.CallbackQuery):
    if call.data == "cancel":
        await bot.edit_message_text(
            call.message.text + "\n\n__Действие отменено__",
            call.message.chat.id,
            call.message.id,
            reply_markup=None,
        )
        user_info.pop(call.message.chat.id)


async def main():
    await bot.infinity_polling()


# if __name__ == "__main__":
#     main()
