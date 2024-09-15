import re
import telebot

from db_req import *
from constants import *
from help_func import *


BOT_TOKEN = "7197713140:AAEHSyZLX3Q-CGU0GzK2r2Q7Z45rmSAHWd8"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def bot_start(message):
    if not (db_is_user_exists(message.from_user.id)):
        db_add_user(message.from_user.id, message)

    bot.send_message(message.chat.id, get_message(MESS_WELCOME), parse_mode='html')

    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_LANG),
        parse_mode='html',
        reply_markup=add_underline_keyboard(but_names=["🇺🇦 Ukrainian", '🇬🇧 English', '🇷🇺 Russian'], row_width=3)
    )
    bot.register_next_step_handler(message, add_user_lang)


def add_user_lang(message):
    if not message.content_type == "text":
        send_exception_type(
            message,
            'text',
            add_user_lang,
            but_names=["🇺🇦 Ukrainian", '🇬🇧 English', '🇷🇺 Russian'],
            row_width=3
        )
        return

    if message.text == "🇺🇦 Ukrainian":
        USER_LANG = 1
    elif message.text == "🇬🇧 English":
        USER_LANG = 0
    elif message.text == "🇷🇺 Russian":
        bot.send_message(message.chat.id,"🖕", parse_mode="html")
        send_exception_mistake(
            message,
            MESS_EX_ENTER_LANG_INCORRECT_LANG,
            add_user_lang,
            but_names=["🇺🇦 Ukrainian", '🇬🇧 English'],
            row_width=2
        )
        return
    else:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_LANG_INCORRECT_LANG,
            add_user_lang,
            but_names=["🇺🇦 Ukrainian", '🇬🇧 English', '🇷🇺 Russian'],
            row_width=3
        )
        return

    db_add_data_to_blank(message.from_user.id, DB_COL_LANG ,message.text.split()[1].lower())

    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_GENDER, message.from_user.id, ),
        reply_markup=add_underline_keyboard(
            but_names=[get_message(BUT_FEMALE, message.from_user.id), get_message(BUT_MALE, message.from_user.id)],
            row_width=2
        )
    )
    bot.register_next_step_handler(message, add_gender)
    return


def add_gender(message):
    if not message.content_type == "text":
        send_exception_type(message,'text', add_gender)
        return

    if message.text != get_message(BUT_MALE, message.from_user.id) and message.text != get_message(BUT_FEMALE, message.from_user.id):
        send_exception_mistake(
            message,
            MESS_EX_ENTER_GENDER,
            add_gender,
            but_names=[get_message(BUT_FEMALE, message.from_user.id), get_message(BUT_MALE, message.from_user.id)],
            row_width=2
        )
        return

    db_add_data_to_blank(
        message.from_user.id, DB_COL_GENDER,
        (GENDER_MALE if message.text == get_message(BUT_MALE, message.from_user.id) else GENDER_FEMALE)
    )

    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_NAME, message.from_user.id),
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, add_name)


def add_name(message):
    if not message.content_type == "text":
        send_exception_type(message, 'text', add_name)
        return

    if not message.text.isalpha(): # or not  db_does_name_exists(name):
        send_exception_mistake(
            message,
            MESS_EX_ENTER_NAME_CONT_NUMS,
            add_name
        )
        return

    name = message.text.strip().capitalize()
    db_add_data_to_blank(message.from_user.id, DB_COL_NAME, name)

    bot.send_message(message.chat.id, get_message(MESS_ENTER_AGE, message.from_user.id))
    bot.register_next_step_handler(message, add_age)
    return


def add_age(message):
    if not message.content_type == "text":
        send_exception_type(message, 'text', add_age)
        return

    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except ValueError:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_AGE_NOT_NUM,
            add_age
        )
        return
    except Exception:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_AGE_LITTLE if age <= 10 else MESS_EX_ENTER_AGE_LARGE,
            add_age
        )
        return

    db_add_data_to_blank(message.from_user.id, DB_COL_AGE, int(message.text))

    bot.send_message(message.chat.id, get_message(MESS_ENTER_CITY, message.from_user.id))
    bot.register_next_step_handler(message, add_city)


def add_city(message):
    if not message.content_type == "text":
        send_exception_type(message, 'text', add_city)
        return

    city = message.text.strip().capitalize()
    if not city.isalpha() or not db_does_city_exists(city):
        send_exception_mistake(
            message,
            MESS_EX_ENTER_CITY_CONT_NUM if not city.isalpha() else MESS_EX_ENTER_CITY_NOT_INT_DB,
            add_city
        )
        return

    db_add_data_to_blank(message.from_user.id, DB_COL_CITY, city)

    bot.send_message(message.chat.id, get_message(MESS_ENTER_DESCR, message.from_user.id))
    bot.register_next_step_handler(message, add_description)


def add_description(message):
    if not message.content_type == "text":
        send_exception_type(message, 'text', add_description)
        return

    description = message.text.strip()
    if len(description) < 20 or len(description) > 300:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_DESCR_TOO_LITTLE if len(description) < 20 else MESS_EX_ENTER_DESCR_TOO_LARGE,
            add_description
        )
        return
    elif "http" in description or "www." in description:
        send_exception_mistake(message, MESS_EX_ENTER_DESCR_CONT_LINK, add_description)
        return
    elif re.search(r'\b\w+\.\w+\b', description):
        for tld in db_get_all_tlds():
            tld = tld[0] # get from tuple
            if tld in description:
                send_exception_mistake(message, MESS_EX_ENTER_DESCR_CONT_LINK, add_description)
                return

    db_add_data_to_blank(message.from_user.id, DB_COL_DESC, message.text)

    bot.send_message(message.chat.id, get_message(MESS_ENTER_PHOTO, message.from_user.id))
    bot.register_next_step_handler(message, add_photo)


def add_photo(message):
    if not message.content_type == "photo":
        send_exception_type(message, 'photo', add_photo)
        return

    file_id = message.photo[-1].file_id
    db_add_data_to_blank(message.from_user.id, "photo", file_id)

    send_user_blank(message, message.from_user.id)


def send_user_blank(message, tg_id):
    user_info = db_get_user_blank_info(tg_id)
    user_all_description = f"""**{user_info[1]}, {user_info[2]}, {user_info[3]}**\n\n{user_info[4]}"""

    bot.send_message(
        message.chat.id,
        get_message(MESS_BLANK_ALMOST_READY, message.from_user.id)
    )
    bot.send_photo(
        message.chat.id,
        user_info[0],  # photo
        caption=user_all_description,
        parse_mode='Markdown' # here can be a mostake if users description contains Markdow simbols
    )
    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_GENDER_TO_SEARCH, message.from_user.id),
        reply_markup=add_underline_keyboard(
            but_names=[get_message(BUT_FEMALE, message.from_user.id), get_message(BUT_MALE, message.from_user.id)],
            row_width=2
        )
    )
    bot.register_next_step_handler(message, add_gender_to_search)


def add_gender_to_search(message):
    if not message.content_type == "text":
        send_exception_type(message, 'text', add_gender_to_search)
        return
    if message.text != get_message(BUT_MALE, message.from_user.id) and message.text != get_message(BUT_FEMALE, message.from_user.id):
        send_exception_mistake(
            message,
            MESS_EX_ENTER_GENDER,
            add_gender_to_search,
            but_names=[get_message(BUT_FEMALE, message.from_user.id), get_message(BUT_MALE, message.from_user.id)],
            row_width=2
            )
        return

    db_add_data_to_blank(
        message.from_user.id,
        DB_COL_PREF_GENDER,
        GENDER_MALE if message.text == get_message(BUT_MALE, message.from_user.id) else GENDER_FEMALE
    )

    bot.send_message(
        message.chat.id,
        get_message(MESS_ENTER_MIN_AGE_TO_SEARCH, message.from_user.id),
        reply_markup=telebot.types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, add_min_age_to_search)


def add_min_age_to_search(message):
    if not message.content_type == "text":
        send_exception_type(message, "text", add_min_age_to_search)
        return
    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except ValueError:
        send_exception_mistake(message, MESS_EX_ENTER_AGE_NOT_NUM, add_min_age_to_search)
        return
    except Exception:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_AGE_LITTLE if age <= 10 else MESS_EX_ENTER_AGE_LARGE,
            add_min_age_to_search
        )
        return

    db_add_data_to_blank(message.from_user.id, DB_COL_PREF_MIN_AGE_TO_SEE, age)

    bot.send_message(message.chat.id, get_message(MESS_ENTER_MAX_AGE_TO_SEARCH, message.from_user.id))
    bot.register_next_step_handler(message, add_max_age_to_search)


def add_max_age_to_search(message):
    if not message.content_type == "text":
        send_exception_type(message, "text", add_max_age_to_search)
        return
    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except ValueError:
        send_exception_mistake(message, MESS_EX_ENTER_AGE_NOT_NUM, add_max_age_to_search)
        return
    except Exception:
        send_exception_mistake(
            message,
            MESS_EX_ENTER_AGE_LITTLE if age <= 10 else MESS_EX_ENTER_AGE_LARGE,
            add_max_age_to_search
        )
        return

    db_add_data_to_blank(message.from_user.id, DB_COL_PREF_MAX_AGE_TO_SEE, age)

    bot.send_message(
        message.chat.id,
        get_message(MESS_LETS_SEARCH, message.from_user.id),
        reply_markup=add_underline_keyboard(
            but_names=[get_message(BUT_PUBLISH_AND_SEARCH, message.from_user.id)],
            row_width=1
        )
    )
    bot.register_next_step_handler(message, start_searching)


def start_searching(message):
    if not message.content_type == "text":
        send_exception_type(message, "text", start_searching)
        return
    if message.text != get_message(BUT_PUBLISH_AND_SEARCH, message.from_user.id):
        send_exception_mistake(
            message,
            MESS_DIDNT_PUBLISHED,
            start_searching,
            but_names=[get_message(BUT_PUBLISH_AND_SEARCH, message.from_user.id)],
            row_width=1
        )
        return

    search_blanks(message)


def search_blanks(message):
    blanks_preferances = get_blanks_preferances(message)
    print(blanks_preferances)
    if blanks_preferances.__len__() != 0:
        show_blank(message, *blanks_preferances[0])
    else:
        bot.send_message(message.chat.id, "There is no more blanks to search(")


def show_blank(message, tg_id_blank, photo, name, age, city, description):
    user_all_description = f"""**{name}, {age}, {city}**\n\n{description}"""

    # message = bot.send_photo(
    #     message.chat.id,
    #     photo,
    #     caption=user_all_description,
    #     parse_mode='Markdown',
    #     reply_markup=add_underline_keyboard(['💕', '👎', '⛔️', '⚙'], row_width=4)
    # )

    bot.send_message(
        message.chat.id,
        user_all_description,
        parse_mode='Markdown',
        reply_markup=add_underline_keyboard(['💕', '👎', '⛔️', '⚙'], row_width=4)
    )

    register_like(message, tg_id_blank)

    bot.register_next_step_handler(message, search_blanks)


def send_exception_type(message, type, method, but_names:list=None, row_width:int=None):
    if but_names is None and row_width is None:
        bot.send_message(
            message.chat.id,
            get_message(EXCEPTIONS[type], message.from_user.id),
            parse_mode="html"
        )
    else:
        bot.send_message(
            message.chat.id,
            get_message(EXCEPTIONS[type], message.from_user.id),
            parse_mode="html",
            reply_markup=add_underline_keyboard(but_names, row_width)
        )
    bot.register_next_step_handler(message, method)


def send_exception_mistake(message, mistake, method, but_names:list=None, row_width:int=None):
    if but_names is None and row_width is None:
        bot.send_message(
            message.chat.id,
            get_message(mistake, message.from_user.id),
            parse_mode="html"
        )
    else:
        bot.send_message(
            message.chat.id,
            get_message(mistake, message.from_user.id),
            parse_mode="html",
            reply_markup=add_underline_keyboard(but_names, row_width)
        )
    bot.register_next_step_handler(message, method)


bot.infinity_polling()



