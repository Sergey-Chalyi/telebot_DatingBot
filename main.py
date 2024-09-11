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

MESS_WELCOME = (
    "<b>Hello👋</b>\n"
    "This bot is to help you with dating💕\n"
    "Let's make your blank!"
)

MESS_ENTER_GENDER = "Enter your gender:"
MESS_EX_ENTER_GENDER = "<b>You have typed the wrong gender!</b>\nEnter your gender:"

MESS_ENTER_NAME = "Enter your name:"
MESS_EX_ENTER_NAME_CONT_NUMS = "<b>The name can`t contain figures!</b>\nEnter your name:"
MESS_EX_ENTER_NAME_NOT_IN_DB = "<b>Such name doesn't exists!</b>\nEnter your name:"

MESS_ENTER_AGE = "Enter your age:"
MESS_EX_ENTER_AGE_LITTLE = "<b>Too little age!</b>\nEnter your age:"
MESS_EX_ENTER_AGE_LARGE = "<b>Too large age!</b>\nEnter your age:"
MESS_EX_ENTER_AGE_NOT_NUM = "<b>Not a number!</b>\nEnter your age:"

MESS_ENTER_CITY = "Enter your city:"
MESS_EX_ENTER_CITY_CONT_NUM = "<b>The city can't contain figures!</b>\nEnter your city:"
MESS_EX_ENTER_CITY_NOT_INT_DB = "<b>Such city doesn't exist!</b>\nEnter your city:"

MESS_ENTER_DESCR = "Enter your description"
MESS_EX_ENTER_DESCR_TOO_LITTLE = "<b>The description is too little!</b>\nEnter your description:"
MESS_EX_ENTER_DESCR_TOO_LARGE = "<b>The description is too large!</b>\nEnter your description:"
MESS_EX_ENTER_DESCR_CONT_LINK = "<b>The description can't contain any links!</b>\nEnter your description:"

MESS_ENTER_PHOTO = "Enter your photo:"
MESS_EX_ENTER_PHOTO_CONT_QR = "<b>Photo can't contain qr codes!</b> Enter your photo:"


BUT_CREATE_NEW_BLANK = "Create new blank!"

BUT_MALE = "Male 🧑🏻"
BUT_FEMALE = "Female 👩🏻"

DB_COL_GENDER = 'gender'
DB_COL_NAME = 'name'
DB_COL_AGE = 'age'
DB_COL_CITY = 'city'
DB_COL_DESC = 'description'

GENDER_MALE = 'm'
GENDER_FEMALE = 'f'

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
    match but_name:
        case BUT_CREATE_NEW_BLANK:
            return "create_blank"

@bot.message_handler(commands=['start'])
def com_start(message):
    # add user private information
    if not (db_req.is_user_exists_in_priv_db(message.from_user.id)):
        # add user to db and show inline buttons
        db_req.add_user_to_priv_db(message.from_user.id, message)

    bot.send_message(message.chat.id,
                     MESS_WELCOME,
                     parse_mode='html',
                     reply_markup = add_inline_keyboard(but_names=[BUT_CREATE_NEW_BLANK], row_width=1)
                     )

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    match callback.data:
        case "create_blank":
            bot.send_message(
                callback.message.chat.id,
                MESS_ENTER_GENDER,
                reply_markup=add_underline_keyboard(
                    but_names=[BUT_FEMALE, BUT_MALE],
                    row_width=2
                )
            )
            bot.register_next_step_handler(callback.message, add_gender)
            return

        case "choose_gender_to_find":
            bot.send_message(callback.message.chat.id, "Witch gender do you want to search (m/f)?")
            bot.register_next_step_handler(callback.message, choose_gender_to_find)
            return

        case "start_searching":
            bot.register_next_step_handler(callback.message, search_blanks)
            return


def add_gender(message):
    if message.text == BUT_MALE or message.text == BUT_FEMALE:
        db_req.add_gender_to_blank(GENDER_MALE if message.text == BUT_MALE else GENDER_FEMALE)
        print("Gender has already added!")

        message = bot.send_message(
            message.chat.id,
            MESS_ENTER_NAME,
        )
        bot.register_next_step_handler(message, add_name)
        # feature: add my nickname as a name
    else:
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_GENDER,
            parse_mode = "html",
            reply_markup=add_underline_keyboard(
                but_names=[BUT_FEMALE, BUT_MALE],
                row_width=2
            )
        )
        bot.register_next_step_handler(message, add_gender)


def add_name(message):
    # checking word on correct form
    name = message.text.strip().capitalize()

    if not name.isalpha() or not db_req.does_name_exists(name):
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_NAME_CONT_NUMS if not name.isalpha() else MESS_EX_ENTER_NAME_NOT_IN_DB,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_name)
        return
    else:
        db_req.add_data_to_blank(DB_COL_NAME, name)
        print("Name has already added!")

        message = bot.send_message(message.chat.id, MESS_ENTER_AGE)
        bot.register_next_step_handler(message, add_age)
        return


def add_age(message):
    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except ValueError as exception:
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_AGE_NOT_NUM,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_age)
        return
    except Exception as exception:
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_AGE_LITTLE if age <= 10 else MESS_EX_ENTER_AGE_LARGE,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_age)
        return

    db_req.add_data_to_blank(DB_COL_AGE, int(message.text))
    print("Age has already added!")

    message = bot.send_message(message.chat.id, MESS_ENTER_CITY)
    bot.register_next_step_handler(message, add_city)


def add_city(message):
    city = message.text.strip().capitalize()
    if not city.isalpha() or not db_req.does_city_exists(city):
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_CITY_CONT_NUM if not city.isalpha() else MESS_EX_ENTER_CITY_NOT_INT_DB,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_city)
        return

    db_req.add_data_to_blank(DB_COL_CITY, message.text)
    print("City has already added!")

    # for the next step
    message = bot.send_message(message.chat.id, MESS_ENTER_DESCR)
    bot.register_next_step_handler(message, add_description)

def add_description(message):
    # checking
    description = message.text.strip()
    if len(description) < 20 or len(description) > 300:
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_DESCR_TOO_LITTLE if len(description) < 20 else MESS_EX_ENTER_DESCR_TOO_LARGE,
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_description)
        return
    elif "http" in description or "www." in description:
        message = bot.send_message(
            message.chat.id,
            MESS_EX_ENTER_DESCR_CONT_LINK,
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
                    MESS_EX_ENTER_DESCR_CONT_LINK,
                    parse_mode="html"
                )
                bot.register_next_step_handler(message, add_description)
                return

    db_req.add_data_to_blank(DB_COL_DESC, message.text)
    print("Description has already added!")

    # for the next step
    message = bot.send_message(message.chat.id, MESS_ENTER_PHOTO)
    bot.register_next_step_handler(message, add_photo)


def add_photo(message):
    # I need to process if user enter not a document, but photo

    # get photo
    file_id = message.document.file_id
    file_info = bot.get_file(file_id=file_id)
    file_path = file_info.file_path
    # download photo
    file = bot.download_file(file_path)
    # validating
    file_metadata = get_metadata(file) # IMPLEMENT this method

    # if file_metadata is None:
    #     message = bot.send_message(message.chat.id,
    #                                "<b>You have sent not a photo!!!</b>"
    #                                "\nSend correct photo:",
    #                                parse_mode="html")
    #     bot.register_next_step_handler(message, add_photo)
    #     return
    # elif not does_person_present_on_photo(file): # IMPLEMENT this method
    #     message = bot.send_message(
    #         message.chat.id,
    #         "<b>You have sent a photo without person on it!!!</b>" "\nSend correct photo:",
    #         parse_mode="html"
    #     )
    #     bot.register_next_step_handler(message, add_photo)
    #     return
    #     # one more: we need to check datatime this photo with the required to check the right person
    if does_photo_contains_qr(file) > 0: # IMPLEMENT this method
        message = bot.send_message(
            message.chat.id,
            "<b>You have sent a photo with qr on it!!!</b>" "\nSend correct photo:",
            parse_mode="html"
        )
        bot.register_next_step_handler(message, add_photo)
        return

    # add photo to db
    db_req.add_data_to_blank("photo", file_id)
    print("Photo has already added!")
    # newt function
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
    print("blank has already added")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Publish and start searching!", callback_data="choose_gender_to_find"))

    bot.send_message(message.chat.id,
                "Do you want to publish your blank and start searching?)",
                     reply_markup=markup)

def choose_gender_to_find(message):
    db_req.add_data_to_blank("preferences_gender", message.text)
    print("Gender to search has already chosen!")
    bot.send_message(message.chat.id, "Print min age of blanks witch you want to see")
    bot.register_next_step_handler(message, choose_min_age_to_find)

def choose_min_age_to_find(message):
    db_req.add_data_to_blank("preferances_to_see_min_age", message.text)
    print("preferances_to_see_min_age has just added!")
    bot.send_message(message.chat.id, "Print max age of blanks witch you want to see")
    bot.register_next_step_handler(message, choose_max_age_to_find)

def choose_max_age_to_find(message):
    db_req.add_data_to_blank("choose_max_age_to_find", message.text)
    print("choose_max_age_to_find has just added!")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Let's start!", callback_data="start_searching"))

    bot.send_message(message.chat.id, "OKEY, that is all! Let's watch the blanks!!!")


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
