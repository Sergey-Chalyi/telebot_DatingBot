import re
from typing import final

import telebot

from functools import partial, wraps

from db_req import *
from constants import *
from help_func import *


BOT_TOKEN = "7197713140:AAEHSyZLX3Q-CGU0GzK2r2Q7Z45rmSAHWd8"
bot = telebot.TeleBot(BOT_TOKEN)
bot.get_updates(offset=0)


def check_message_type(content_type="text", but_names:list=None, row_width:int=None):
    def decorator(func):
        @wraps(func)
        def wrapper(message, *args, **kwargs):
            if message.content_type != 'text':
                if but_names is None and row_width is None:
                    send_exception_type(message, content_type, func)
                else:
                    send_exception_type(
                        message,
                        content_type,
                        func,
                        but_names=but_names,
                        row_width=row_width
                    )
                return
            return func(message, *args, **kwargs)
        return wrapper
    return decorator


# bot starts working here
@bot.message_handler(commands=['start'])
def bot_start(message):
    if not (db_is_user_exists(message.from_user.id)):
        db_add_user(message.from_user.id, message)

    bot.send_message(message.chat.id, get_message(MESS_WELCOME), parse_mode='html')
    add_username(message)

def add_username(message):
    if bot.get_chat(message.from_user.id).username is None:
        bot.send_message(
            message.chat.id,
            "You haven't got username\n"
            "Add username to your profile to bot works correctly and then press on the button",
            reply_markup=add_underline_keyboard(['I have just added username!'], row_width=1)
        )
        bot.register_next_step_handler(message, check_username_on_existing)
    else:
        bot.send_message(
            message.chat.id,
            get_message(MESS_ENTER_LANG),
            parse_mode='html',
            reply_markup=add_underline_keyboard(but_names=["🇺🇦 Ukrainian", '🇬🇧 English', '🇷🇺 Russian'], row_width=3)
        )
        bot.register_next_step_handler(message, add_user_lang)

def check_username_on_existing(message):
    if not message.content_type == "text":
        send_exception_type(
            message,
            'text',
            check_username_on_existing,
            but_names=["I have just added username!"],
            row_width=1
        )
        return
    if message.text != "I have just added username!":
        bot.send_message(
            message.chat.id,
            "You didn't pressed on the button!",
            parse_mode="html",
            reply_markup=add_underline_keyboard(["I have just added username!"])
        )
        bot.register_next_step_handler(message, check_username_on_existing)
        return

    if bot.get_chat(message.from_user.id).username is None:
        bot.send_message(
            message.chat.id,
            "You haven't added the username\n"
            "Add username to your profile to bot works correctly and then press on the button",
            reply_markup=add_underline_keyboard(['I have just added username!'], row_width=1)
        )
        bot.register_next_step_handler(message, check_username_on_existing)
    else:
        bot.send_message(
            message.chat.id,
            get_message(MESS_ENTER_LANG),
            parse_mode='html',
            reply_markup=add_underline_keyboard(but_names=["🇺🇦 Ukrainian", '🇬🇧 English', '🇷🇺 Russian'], row_width=3)
        )
        bot.register_next_step_handler(message, add_user_lang)


@check_message_type(content_type='text')
def add_user_lang(message):
    if message.text == "🇺🇦 Ukrainian": USER_LANG = 1
    elif message.text == "🇬🇧 English": USER_LANG = 0
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


@check_message_type(content_type='text')
def add_gender(message):
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


@check_message_type(content_type='text')
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


@check_message_type(content_type='text')
def add_age(message):
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


@check_message_type(content_type='text')
def add_city(message):
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


@check_message_type(content_type='text')
def add_description(message):
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


# @check_message_type(content_type='photo')
def add_photo(message):
    if message.content_type != 'photo':
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


@check_message_type(content_type='text')
def add_gender_to_search(message):
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


@check_message_type(content_type='text')
def add_min_age_to_search(message):
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


@check_message_type(content_type='text')
def add_max_age_to_search(message):
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


@bot.message_handler(commands=['search'])
@check_message_type(content_type='text')
def start_searching(message):
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


@check_message_type(content_type='text')
def search_blanks(message):
    blanks_preferances = del_watched_blanks(get_blanks_preferances(message), message.from_user.id)

    if blanks_preferances.__len__() != 0:
        if check_mutual_likes_of_my_blank(message):
            return

        if check_first_likes_of_my_blank(message):
             return

        # show next blank
        show_blank(message, *blanks_preferances[0])

    else:
        # here I need to work on it
        bot.send_message(message.chat.id, "There is no more blanks to search(")

def check_mutual_likes_of_my_blank(message):
    mutual_likes = get_list_of_mutual_likes(message.from_user.id)

    if len(mutual_likes) > 0:
        bot.send_message(
            message.chat.id,
            f"You have liked mutually {len(mutual_likes)} {'time' if len(mutual_likes) == 1 else 'times'}"
            f"\nDo you want to see who has liked you?",
            reply_markup=add_underline_keyboard(but_names=['yes', 'no'], row_width=2)
        )
        bot.register_next_step_handler(message, lambda msg: do_show_liked_blanks(msg, mutual_likes))
        return True
    return False


def do_show_liked_blanks(message, mutual_likes):
    if message.text == 'yes':
        show_mutually_liked_blanks(message, mutual_likes)
        # maybe here we need to place add watched field into db
    elif message.text == 'no':
        # add info to like db that user did want to see the blanks
        make_all_blanks_watched(message, mutual_likes)
        bot.send_message(
            message.chat.id,
            "Okey!"
        )
        search_blanks(message)

def make_all_blanks_watched(message, mutual_likes):
    for blank in mutual_likes:
        tg_id_blank = blank[0]
        db_make_blank_watched(message.from_user.id, tg_id_blank)

def show_mutually_liked_blanks(message, mutual_likes: list):
    mutual_likes = get_list_of_mutual_likes(message.from_user.id)
    if len(mutual_likes) > 0:
        show_mutually_liked_blank(message, mutual_likes)
    else:
        bot.send_message(
            message.chat.id,
            "That is all, do you want to continue search new blanks?",
            reply_markup=add_underline_keyboard(but_names=['💕', '👎'], row_width=2)
        )
        bot.register_next_step_handler(message, choose_continue)

def show_mutually_liked_blank(message, mutual_likes):
    tg_id_blank, photo, name, age, city, description = mutual_likes[0]
    user_all_description = f"""**{name}, {age}, {city}**\n\n{description}"""

    message = bot.send_photo(
        message.chat.id,
        photo,
        caption=user_all_description,
        parse_mode='Markdown',
        reply_markup=add_underline_keyboard(['💕', '👎', '⛔️', '⚙'], row_width=4)
    )

    # send blank

    # bot.send_message(
    #     message.chat.id,
    #     user_all_description,
    #     parse_mode='Markdown',
    #     reply_markup=add_underline_keyboard(['NEXT'])
    # )
    send_link_to_blank(message, tg_id_blank)
    make_blank_watched(message, tg_id_blank)

    bot.register_next_step_handler(message, lambda msg: show_mutually_liked_blanks(msg, mutual_likes))

@check_message_type(content_type='text')
def choose_continue(message):
    if message.text not in ['💕', '👎']:
        send_exception_mistake(message, "not an emoji", choose_continue)
        return

    if message.text == '💕':
        bot.send_message(message.chat.id,"Okey, let's continue!")
        search_blanks(message)
        return
    elif message.text == '👎':
        # here I need to imagine something
        bot.send_message(
            message.chat.id,
            "Okey, I hope I helped you with your aims))\n"
            "Come back if you would like to find someone!",
            reply_markup=add_underline_keyboard(['Start search again'])
        )
        return



def check_first_likes_of_my_blank(message):
    first_likes = get_list_of_first_likes(message.from_user.id)
    if len(first_likes) > 0:
        bot.send_message(
            message.chat.id,
            f"You have liked {len(first_likes)} {'time' if len(first_likes) == 1 else 'times'}"
            f"\nDo you want to see who has liked you?",
            reply_markup=add_underline_keyboard(but_names=['yes', 'no'], row_width=2)
        )
        bot.register_next_step_handler(message, lambda msg: do_show_blanks(msg, first_likes))
        return True
    return False


def do_show_blanks(message, first_likes):
    if message.text == 'yes':
        show_liked_blanks(message, first_likes)
        # maybe here we need to place add watched field into db
    elif message.text == 'no':
        # add info to like db that user did want to see the blanks
        make_all_blanks_watched(message, first_likes) # here I think I need to so something better
        bot.send_message(
            message.chat.id,
            "Okey!"
        )
        search_blanks(message)


def show_liked_blanks(message, first_likes):
    first_likes = get_list_of_first_likes(message.from_user.id)
    if len(first_likes) > 0:
        show_liked_blank(message, first_likes)
    else:
        bot.send_message(
            message.chat.id,
            "That is all, do you want to continue search new blanks?",
            reply_markup=add_underline_keyboard(but_names=['💕', '👎'], row_width=2)
        )
        bot.register_next_step_handler(message, choose_continue)


def show_liked_blank(message, first_likes):
    tg_id_blank, photo, name, age, city, description = first_likes[0]
    user_all_description = f"""**{name}, {age}, {city}**\n\n{description}"""

    message = bot.send_photo(
        message.chat.id,
        photo,
        caption=user_all_description,
        parse_mode='Markdown',
        reply_markup=add_underline_keyboard(['💕', '👎', '⛔️', '⚙'], row_width=4)
    )

    # send blank

    # bot.send_message(
    #     message.chat.id,
    #     user_all_description,
    #     parse_mode='Markdown',
    #     reply_markup=add_underline_keyboard(['💕', '👎', '⛔️', '⚙'], row_width=4)
    # )
    bot.register_next_step_handler(message, lambda msg: register_first_like(msg, first_likes))


def register_first_like(message, first_likes):
    tg_id_blank = first_likes[0][0]
    if not message.content_type == "text":
        send_exception_type(message, "text", lambda msg: register_like(msg, tg_id_blank))
        return
    if message.text not in ['💕', '👎', '⛔️', '⚙']:
        send_exception_mistake(message, "not an emoji", lambda msg: register_like(msg, tg_id_blank))
        return

    if message.text == '💕' or message.text == '👎':
        db_add_users_likes(
            tg_id_user=message.from_user.id,
            tg_id_blank=tg_id_blank,
            like= 'yes' if message.text == '💕' else "no"
        )
        if message.text == '💕':
            send_link_to_blank(message, tg_id_blank)
    elif message.text == '⛔️':
        pass
    elif message.text == '⚙':
        pass
    else:
        pass

    make_blank_watched(message, tg_id_blank)
    show_liked_blanks(message, first_likes)



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

    bot.register_next_step_handler(message, lambda msg: register_like(msg, tg_id_blank))


def register_like(message, tg_id_blank):
    if not message.content_type == "text":
        send_exception_type(message, "text", lambda msg: register_like(msg, tg_id_blank))
        return
    if message.text not in ['💕', '👎', '⛔️', '⚙']:
        send_exception_mistake(message, "not an emoji", lambda msg: register_like(msg, tg_id_blank))
        return

    if message.text == '💕' or message.text == '👎':
        db_add_users_likes(
            tg_id_user=message.from_user.id,
            tg_id_blank=tg_id_blank,
            like= 'yes' if message.text == '💕' else "no"
        )
    elif message.text == '⛔️':
        pass
    elif message.text == '⚙':
        pass
    else:
        pass

    search_blanks(message)












def make_blank_watched(message, tg_id_blank):
    db_make_blank_watched(message.from_user.id, tg_id_blank)










def send_link_to_blank(message, tg_id_blank):
    user_to_show = bot.get_chat(tg_id_blank)
    nickname = user_to_show.username
    first_name = user_to_show.first_name
    if nickname:
        bot.send_message(
            message.chat.id,
            f"[{f"@{nickname}"}]({f"https://t.me/{nickname}"})",
            parse_mode='Markdown'
        )
    else:
        bot.send_message(
            message.chat.id,
            f"[{first_name}]({f"https://t.me/user?id={tg_id_blank}"})",
            parse_mode='Markdown'
        )


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



