import telebot
from db_req import *
from constants import *

def get_message(mistake_message, tg_id = None):
    if tg_id == None:
        return MESSAGES[mistake_message][0]
    else:
        return MESSAGES[mistake_message][LANGUAGES[db_get_user_lang(tg_id)]]


def add_underline_keyboard(but_names: list, row_width: int = 2):
    """Create UNDERLINE keyboard with one line of buttons"""

    markup = telebot.types.ReplyKeyboardMarkup(row_width=row_width)

    buttons = []
    for but_name in but_names:
        buttons.append(telebot.types.KeyboardButton(but_name))
    markup.add(*buttons)

    return markup


def get_blanks_preferances(message):
    blanks_preferances = db_get_blanks_preferances(
        tg_id=message.from_user.id,
        gender=db_get_user_info(col_name="preferences_gender", tg_id=message.from_user.id),
        min_age=db_get_user_info(col_name="preferances_to_see_min_age", tg_id=message.from_user.id),
        max_age=db_get_user_info(col_name="preferances_to_see_max_age", tg_id=message.from_user.id)
    )
    return blanks_preferances


def del_watched_blanks(blanks_preferances: list, tg_id_user: int):
    watched_blanks = db_get_users_likes(tg_id_user)
    final_blanks_list = []
    for blank in blanks_preferances:
        if blank[0] not in watched_blanks:
            final_blanks_list.append(blank)
    return final_blanks_list


def get_list_of_mutual_likes(user_id):
    positive_user_likes = get_all_positive_user_likes(user_id)
    positive_likes_myself = get_all_positive_likes_myself(user_id)
    return list(set(positive_user_likes).intersection(set(positive_likes_myself)))

