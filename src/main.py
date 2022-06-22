from telebot import types
from telebot.async_telebot import AsyncTeleBot
from asyncio import run
import config
import reghandler as reg
import dbhandler as db
import webhandler as wb
import datetime

# Owner info
owner = config.OWNER

bot = AsyncTeleBot(config.TOKEN, parse_mode=config.PARSE_MODE)

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

hello_sticker = open("assets/Hello.webp", "rb")

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
async def start_handler(message: types.Message):
    await bot.send_sticker(message.chat.id, hello_sticker)
    await bot.send_message(
        message.chat.id,
        f"Привет, *{message.from_user.first_name}*!\n"
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
            "Введи свой *логин* на платформе",
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
            + "Сперва зарегистрируйся, введя команду /register",
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


@bot.message_handler(commands=["agenda"])
async def send_agenda(message: types.Message):
    user_info = db.read_from_db(str(message.chat.id))
    if not user_info:
        await bot.send_message(
            message.chat.id,
            "Для получения сводки необходимо сперва зарегистрироваться. Ты можешь сделать это с помощью команды /register.",
        )
    else:
        messg = await bot.send_message(
            message.chat.id, "*Собираю информацию...*\n\n" + "_[1/2] - авторизация_"
        )
        d = datetime.datetime.today()
        d = d.strftime("%d.%m.%y")
        events = wb.get_today_events(user_info["login"], user_info["password"])
        if events is None:
            await bot.edit_message_text(
                "Возникли проблемы с авторизацией. Попробуй позже.\n\n"
                + f"_Если не получится позже, напиши *Создателю*: @{config.OWNER}_",
                message.chat.id,
                messg.id,
            )
        else:
            await bot.edit_message_text(
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
            await bot.edit_message_text(msg, messg.chat.id, messg.id)


async def handle_unknown(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    write_me_button = types.InlineKeyboardButton("Напиши!", "telegram.me/" + owner)
    markup.add(write_me_button)
    await bot.send_message(
        message.chat.id,
        "Такой команды я не знаю. Возможно, мой Создатель её ещё не реализовал...\n\n"
        + f"Если хочешь, чтобы Создатель реализовал эту команду, *напиши* ему: @{owner}",
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


def check_agenda_text(message: types.Message):
    if message.text == "Сводка":
        return True


@bot.message_handler(content_types=["text"], func=check_agenda_text)
async def agenda_text_handler(message: types.Message):
    await send_agenda(message)


@bot.message_handler(content_types=["text"])
async def text_handler(message: types.Message):
    if user_info.get(str(message.chat.id), None) is not None:
        if len(user_info.get(str(message.chat.id))) == 1:
            user_info.get(str(message.chat.id)).append(message.text.strip().lower())
            await bot.send_message(
                message.chat.id,
                "Теперь введи *пароль* от платформы\n\n_Не бойся, я шифрую данные, так что не смогу их применить_",
                reply_markup=reg.cancel_markup_inline,
            )
        elif len(user_info.get(str(message.chat.id))) == 2:
            tmp_message = await bot.send_message(
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
                await bot.edit_message_text(
                    f"Ты зарегистрировался под ником *{user_info.get(str(message.chat.id))[1]}*\n\nДля отмены регистрации выполни команду /unregister"
                    + "\n*ОБЯЗАТЕЛЬНО* удали сообщение с паролем в целях конфиденциальности!",
                    message.chat.id,
                    tmp_message.id,
                )
                user_info.pop(str(message.chat.id), [])
            else:
                await bot.edit_message_text(
                    "Мне не удалось авторизоваться на платформе с этими данными. Попробуй ещё раз.",
                    message.chat.id,
                    tmp_message.id,
                )
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
            call.message.text + "\n\n_Действие отменено_",
            call.message.chat.id,
            call.message.id,
            reply_markup=None,
        )
        user_info.pop(call.message.chat.id)


run(bot.infinity_polling())
