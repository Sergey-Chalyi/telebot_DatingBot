import io
import re
from io import BytesIO
from PIL import Image
from PIL.ImageChops import constant
from pyzbar.pyzbar import decode

import telebot
import db_req


BOT_TOKEN = "7197713140:AAEHSyZLX3Q-CGU0GzK2r2Q7Z45rmSAHWd8"
bot = telebot.TeleBot(BOT_TOKEN)


user_lang = 0 # english language (default)

MESS_WELCOME = "MESS_WELCOME"

MESS_ENTER_GENDER = "MESS_ENTER_GENDER"
MESS_EX_ENTER_GENDER = "MESS_EX_ENTER_GENDER"

MESS_ENTER_NAME = "MESS_ENTER_NAME"
MESS_EX_ENTER_NAME_CONT_NUMS = "MESS_EX_ENTER_NAME_CONT_NUMS"
MESS_EX_ENTER_NAME_NOT_IN_DB = "MESS_EX_ENTER_NAME_NOT_IN_DB"

MESS_ENTER_AGE = "MESS_ENTER_AGE"
MESS_EX_ENTER_AGE_LITTLE = "MESS_EX_ENTER_AGE_LITTLE"
MESS_EX_ENTER_AGE_LARGE = "MESS_EX_ENTER_AGE_LARGE"
MESS_EX_ENTER_AGE_NOT_NUM = "MESS_EX_ENTER_AGE_NOT_NUM"

MESS_ENTER_CITY = "MESS_ENTER_CITY"
MESS_EX_ENTER_CITY_CONT_NUM = "MESS_EX_ENTER_CITY_CONT_NUM"
MESS_EX_ENTER_CITY_NOT_INT_DB = "MESS_EX_ENTER_CITY_NOT_INT_DB"

MESS_ENTER_DESCR = "MESS_ENTER_DESCR"
MESS_EX_ENTER_DESCR_TOO_LITTLE = "MESS_EX_ENTER_DESCR_TOO_LITTLE"
MESS_EX_ENTER_DESCR_TOO_LARGE = "MESS_EX_ENTER_DESCR_TOO_LARGE"
MESS_EX_ENTER_DESCR_CONT_LINK = "MESS_EX_ENTER_DESCR_CONT_LINK"

MESS_ENTER_PHOTO = "MESS_ENTER_PHOTO"
MESS_EX_ENTER_PHOTO_CONT_QR = "MESS_EX_ENTER_PHOTO_CONT_QR"

MESS_SET_LANG = "BUT_SET_LANG"
MESS_EX_SET_LANG_INCORRECT_LANG = "MESS_EX_SET_LANG_INCORRECT_LANG"

BUT_CREATE_NEW_BLANK = "BUT_CREATE_NEW_BLANK"
BUT_MALE = "BUT_MALE"
BUT_FEMALE = "BUT_FEMALE"


DB_COL_GENDER = 'gender'
DB_COL_NAME = 'name'
DB_COL_AGE = 'age'
DB_COL_CITY = 'city'
DB_COL_DESC = 'description'


GENDER_MALE = 'm'
GENDER_FEMALE = 'f'


messages = {
    MESS_WELCOME: (
        "<b>Hello👋</b>\nThis bot is to help you with dating💕\nLet's make your blank!",
        "<b>Привіт👋</b>\nЦей бот допоможе вам із знайомствами💕\nДавайте створимо вашу анкету!"
    ),
    MESS_ENTER_GENDER: (
        "Enter your gender:",
        "Введіть вашу стать:"
    ),
    MESS_EX_ENTER_GENDER: (
        "<b>You have typed the wrong gender ❌</b>\nEnter your gender:",
        "<b>Ви ввели неправильну стать ❌</b>\nВведіть вашу стать:"
    ),
    MESS_ENTER_NAME: (
        "Enter your name: 📝",
        "Введіть ваше ім'я: 📝"
    ),
    MESS_EX_ENTER_NAME_CONT_NUMS: (
        "<b>The name can't contain figures ❌</b>\nEnter your name:",
        "<b>Ім'я не може містити цифри ❌</b>\nВведіть ваше ім'я:"
    ),
    MESS_EX_ENTER_NAME_NOT_IN_DB: (
        "<b>Such name doesn't exist ❌</b>\nEnter your name:",
        "<b>Таке ім'я не існує ❌</b>\nВведіть ваше ім'я:"
    ),
    MESS_ENTER_AGE: (
        "Enter your age: 🎂",
        "Введіть ваш вік: 🎂"
    ),
    MESS_EX_ENTER_AGE_LITTLE: (
        "<b>Too little age ❌</b>\nEnter your age:",
        "<b>Занадто малий вік ❌</b>\nВведіть ваш вік:"
    ),
    MESS_EX_ENTER_AGE_LARGE: (
        "<b>Too large age ❌</b>\nEnter your age:",
        "<b>Занадто великий вік ❌</b>\nВведіть ваш вік:"
    ),
    MESS_EX_ENTER_AGE_NOT_NUM: (
        "<b>Not a number ❌</b>\nEnter your age:",
        "<b>Це не число ❌</b>\nВведіть ваш вік:"
    ),
    MESS_ENTER_CITY: (
        "Enter your city: 🌆",
        "Введіть ваше місто: 🌆"
    ),
    MESS_EX_ENTER_CITY_CONT_NUM: (
        "<b>The city can't contain figure ❌</b>\nEnter your city:",
        "<b>Місто не може містити цифри ❌</b>\nВведіть ваше місто:"
    ),
    MESS_EX_ENTER_CITY_NOT_INT_DB: (
        "<b>Such city doesn't exist ❌</b>\nEnter your city:",
        "<b>Таке місто не існує ❌</b>\nВведіть ваше місто:"
    ),
    MESS_ENTER_DESCR: (
        "Enter your description: 📝",
        "Введіть ваш опис: 📝"
    ),
    MESS_EX_ENTER_DESCR_TOO_LITTLE: (
        "<b>The description is too little ❌</b>\nEnter your description:",
        "<b>Опис занадто короткий ❌</b>\nВведіть ваш опис:"
    ),
    MESS_EX_ENTER_DESCR_TOO_LARGE: (
        "<b>The description is too large ❌</b>\nEnter your description:",
        "<b>Опис занадто довгий ❌</b>\nВведіть ваш опис:"
    ),
    MESS_EX_ENTER_DESCR_CONT_LINK: (
        "<b>The description can't contain any links ❌</b>\nEnter your description:",
        "<b>Опис не може містити посилання ❌</b>\nВведіть ваш опис:"
    ),
    MESS_ENTER_PHOTO: (
        "Enter your photo: 📸",
        "Завантажте ваше фото: 📸"
    ),
    MESS_EX_ENTER_PHOTO_CONT_QR: (
        "<b>Photo can't contain QR codes ❌</b>\nEnter your photo:",
        "<b>Фото не може містити QR-коди ❌</b>\nЗавантажте ваше фото:"
    ),
    MESS_SET_LANG: (
        "Choose your language: 🌎",
        "Виберіть свою мову: 🌎"
    ),
    MESS_EX_SET_LANG_INCORRECT_LANG : (
        "<b>You have typed incorrect language ❌</b>\nEnter your language: 🌎",
        "<b>Ви ввели неправильну мову ❌</b>\nВведіть вашу мову: 🌎"
    ),

    BUT_CREATE_NEW_BLANK: (
        "Create new blank! 🆕",
        "Створити нову анкету! 🆕"
    ),
    BUT_MALE: (
        "Male 🧑🏻",
        "Чоловік 🧑🏻"
    ),
    BUT_FEMALE: (
        "Female 👩🏻",
        "Жінка 👩🏻"
    )
}


def get_message(message):
    return messages[message][user_lang]


def add_inline_keyboard(but_names: list, row_width: int):
    """Create INLINE keyboard"""

    markup = telebot.types.InlineKeyboardMarkup(row_width=row_width)

    buttons = []
    for but_name in but_names:
        buttons.append(telebot.types.InlineKeyboardButton(but_name, callback_data=get_callback_name(but_name)))
    markup.add(*buttons)

    return markup


def add_underline_keyboard(but_names: list, row_width: int):
    """Create UNDERLINE keyboard with one line of buttons"""

    markup = telebot.types.ReplyKeyboardMarkup(row_width=row_width)

    buttons = []
    for but_name in but_names:
        buttons.append(telebot.types.KeyboardButton(but_name))
    markup.add(*buttons)

    return markup


def get_callback_name(but_name):
    if but_name == get_message(BUT_CREATE_NEW_BLANK):
        return "create_blank"


@bot.message_handler(commands=['start'])
def bot_start(message):
    if not (db_req.is_user_exists_in_priv_db(message.from_user.id)):
        db_req.add_user_to_priv_db(message.from_user.id, message)

    bot.send_message(
        message.chat.id,
        get_message(MESS_WELCOME),
        parse_mode='html'
    )

    message = bot.send_message(
        message.chat.id,
        get_message(MESS_SET_LANG),
        parse_mode='html',
        reply_markup=add_underline_keyboard(but_names=["🇺🇦 Ukrainian", '🇬🇧 English', ], row_width=4)
    )

    bot.register_next_step_handler(message, choose_lang)


def choose_lang(message):
    global user_lang

    if message.text == "🇺🇦 Ukrainian":
        user_lang = 1
    elif message.text == "🇬🇧 English":
        user_lang = 0
    else:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_SET_LANG_INCORRECT_LANG),
            parse_mode="html",
            reply_markup=add_underline_keyboard(but_names=["🇺🇦 Ukrainian", '🇬🇧 English', ], row_width=4)
        )
        bot.register_next_step_handler(message, choose_lang)
        return

    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_GENDER),
        reply_markup=add_underline_keyboard(
            but_names=[get_message(BUT_FEMALE), get_message(BUT_MALE)],
            row_width=2
        )
    )
    bot.register_next_step_handler(message, add_gender)
    return




@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    match callback.data:
        case "create_blank":
            bot.send_message(
                callback.message.chat.id,
                get_message(MESS_ENTER_GENDER),
                reply_markup=add_underline_keyboard(
                    but_names=[get_message(BUT_FEMALE), get_message(BUT_MALE)],
                    row_width=2
                )
            )
            bot.register_next_step_handler(callback.message, add_gender)
            return

        case "set_language":
            bot.send_message(
                callback.message.chat.id,
                get_message(MESS_ENTER_GENDER),
                reply_markup=add_underline_keyboard(
                    but_names=[get_message(BUT_FEMALE), get_message(BUT_MALE)],
                    row_width=2
                )
            )
            bot.register_next_step_handler(callback.message, add_gender)
            return
            return

        case "choose_gender_to_find":
            bot.send_message(callback.message.chat.id, "Which gender do you want to search (m/f)?")
            bot.register_next_step_handler(callback.message, choose_gender_to_find)
            return

        case "start_searching":
            bot.register_next_step_handler(callback.message, search_blanks)
            return

def add_gender(message):
    if message.text == get_message(BUT_MALE) or message.text == get_message(BUT_FEMALE):
        db_req.add_gender_to_blank(GENDER_MALE if message.text == BUT_MALE else GENDER_FEMALE)
        print("Gender has already added!")

        message = bot.send_message(
            message.chat.id,
            get_message(MESS_ENTER_NAME)
        )
        bot.register_next_step_handler(message, add_name)
    else:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_GENDER),
            parse_mode="html",
            reply_markup=add_underline_keyboard(
                but_names=[get_message(BUT_FEMALE), get_message(BUT_MALE)],
                row_width=2
            )
        )
        bot.register_next_step_handler(message, add_gender)

def add_name(message):
    name = message.text.strip().capitalize()

    if not name.isalpha() or not db_req.does_name_exists(name):
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_NAME_CONT_NUMS) if not name.isalpha() else get_message(MESS_EX_ENTER_NAME_NOT_IN_DB),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_name)
        return
    else:
        db_req.add_data_to_blank(DB_COL_NAME, name)
        print("Name has already added!")

        message = bot.send_message(message.chat.id, get_message(MESS_ENTER_AGE))
        bot.register_next_step_handler(message, add_age)
        return

def add_age(message):
    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except ValueError:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_AGE_NOT_NUM),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_age)
        return
    except Exception:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_AGE_LITTLE) if age <= 10 else get_message(MESS_EX_ENTER_AGE_LARGE),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_age)
        return

    db_req.add_data_to_blank(DB_COL_AGE, int(message.text))
    print("Age has already added!")

    message = bot.send_message(message.chat.id, get_message(MESS_ENTER_CITY))
    bot.register_next_step_handler(message, add_city)

def add_city(message):
    city = message.text.strip().capitalize()
    if not city.isalpha() or not db_req.does_city_exists(city):
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_CITY_CONT_NUM) if not city.isalpha() else get_message(MESS_EX_ENTER_CITY_NOT_INT_DB),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_city)
        return

    db_req.add_data_to_blank(DB_COL_CITY, message.text)
    print("City has already added!")

    message = bot.send_message(message.chat.id, get_message(MESS_ENTER_DESCR))
    bot.register_next_step_handler(message, add_description)

def add_description(message):
    description = message.text.strip()
    if len(description) < 20 or len(description) > 300:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_DESCR_TOO_LITTLE) if len(description) < 20 else get_message(MESS_EX_ENTER_DESCR_TOO_LARGE),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_description)
        return
    elif "http" in description or "www." in description:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_DESCR_CONT_LINK),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_description)
        return
    elif re.search(r'\b\w+\.\w+\b', description):
        for tld in db_req.get_all_tlds():
            tld = tld[0] # get from tuple
            if tld in description:
                message = bot.send_message(
                    message.chat.id,
                    get_message(MESS_EX_ENTER_DESCR_CONT_LINK),
                    parse_mode="html"
                )
                bot.register_next_step_handler(message, add_description)
                return

    db_req.add_data_to_blank(DB_COL_DESC, message.text)
    print("Description has already added!")

    message = bot.send_message(message.chat.id, get_message(MESS_ENTER_PHOTO))
    bot.register_next_step_handler(message, add_photo)

def add_photo(message):
    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    else:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_PHOTO_CONT_QR),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_photo)
        return

    file_info = bot.get_file(file_id=file_id)
    file_path = file_info.file_path
    file = bot.download_file(file_path)

    if does_photo_contains_qr(file) > 0:
        message = bot.send_message(
            message.chat.id,
            get_message(MESS_EX_ENTER_PHOTO_CONT_QR),
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_photo)
        return

    db_req.add_data_to_blank("photo", file_id)
    print("Photo has already added!")
    get_all_user_information(message, message.from_user.id)

def does_photo_contains_qr(file):
    return len(decode(Image.open(BytesIO(file))))

def get_metadata(file):
    return Image.open(io.BytesIO(file))._getexif()

def does_person_present_on_photo(file):
    pass

def get_all_user_information(message, tg_id):
    user_info = db_req.get_user_blank_info(tg_id)
    user_all_description = f"""**{user_info[1]}, {user_info[2]}, {user_info[3]}**\n\n{user_info[4]}"""

    bot.send_message(message.chat.id, "Your blank is ready! Here it is!")
    bot.send_photo(
        message.chat.id,
        user_info[0],  # photo
        caption=user_all_description,
        parse_mode='Markdown'
    )
    print("Blank has already added")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(get_message("Publish and start searching!"), callback_data="choose_gender_to_find"))

    bot.send_message(message.chat.id,
                     get_message("Do you want to publish your blank and start searching?)"),
                     reply_markup=markup)

def choose_gender_to_find(message):
    db_req.add_data_to_blank("preferences_gender", message.text)
    print("Gender to search has already chosen!")
    bot.send_message(message.chat.id, "Print min age of blanks which you want to see")
    bot.register_next_step_handler(message, choose_min_age_to_find)

def choose_min_age_to_find(message):
    db_req.add_data_to_blank("preferances_to_see_min_age", message.text)
    print("Preferances_to_see_min_age has just added!")
    bot.send_message(message.chat.id, "Print max age of blanks which you want to see")
    bot.register_next_step_handler(message, choose_max_age_to_find)

def choose_max_age_to_find(message):
    db_req.add_data_to_blank("choose_max_age_to_find", message.text)
    print("Choose_max_age_to_find has just added!")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(get_message("Let's start!"), callback_data="start_searching"))

    bot.send_message(message.chat.id, get_message("OKEY, that is all! Let's watch the blanks!!!"))

def search_blanks(message):
    pass

bot.infinity_polling()

def throw_error():
    pass

def create_inline_keyboard(buttons):
    markup = telebot.types.InlineKeyboardMarkup()
    for text, callback_data in buttons:
        markup.add(telebot.types.InlineKeyboardButton(text, callback_data=callback_data))
    return markup

def create_reply_keyboard(buttons):
    markup = telebot.types.ReplyKeyboardMarkup()
    for text, callback_data in buttons:
        markup.add(telebot.types.KeyboardButton(text))
    return markup

