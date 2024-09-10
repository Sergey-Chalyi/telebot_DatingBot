import io
import re
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode

import telebot
import db_req


BOT_TOKEN = "7197713140:AAEHSyZLX3Q-CGU0GzK2r2Q7Z45rmSAHWd8"

bot = telebot.TeleBot(BOT_TOKEN)

WELCOME_MESSAGE = (
    "<b>Hello👋</b>\n"
    "This bot is to help you with dating💕\n"
    "Let's make your blank!"
)

GENDER_PROMT = "Enter your gender:"
NAME_PROMT = "Enter your name:"

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

@bot.message_handler(commands=['start'])
def com_start(message):
    # add user private information
    if not (db_req.is_user_exists_in_priv_db(message.from_user.id)):
        # add user to db and show inline buttons
        db_req.add_user_to_priv_db(message.from_user.id, message)

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Create new blank!", callback_data = "create_blank"))

    bot.send_message(message.chat.id,
                     WELCOME_MESSAGE,
                     parse_mode='html',
                     reply_markup=create_inline_keyboard([("Create new blank!", "add_gender")])
                     )

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "add_gender":
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        but1 = telebot.types.KeyboardButton("Male 🧑🏻")
        but2 = telebot.types.KeyboardButton("Female 👩🏻")
        markup.add(but2, but1)

        bot.send_message(callback.message.chat.id, "Enter your gender:", reply_markup=markup)
        bot.register_next_step_handler(callback.message, add_gender)
    elif callback.data == "choose_gender_to_find":
        bot.send_message(callback.message.chat.id, "Witch gender do you want to search (m/f)?")
        bot.register_next_step_handler(callback.message, choose_gender_to_find)
    elif callback.data == "start_searching":
        bot.register_next_step_handler(callback.message, search_blanks)


def add_gender(message):
    if message.text == "Male 🧑🏻":
        gender = "m"
        db_req.add_gender_to_blank("m")
        print("Gender has already added!")
        message = bot.send_message(message.chat.id,
                                    "Enter your name:",
                                    reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_name)
        # feature: add my nickname as a name
    elif message.text == "Female 👩🏻":
        db_req.add_gender_to_blank('f')
        print("Gender has already added!")
        message = bot.send_message(message.chat.id,
                                   "Enter your name:",
                                   reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_name)
        # feature: add my nickname as a name
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=5)
        but1 = telebot.types.KeyboardButton("Male 🧑🏻")
        but2 = telebot.types.KeyboardButton("Female 👩🏻")
        markup.add(but2, but1)
        message = bot.send_message(message.chat.id, "<b>You have typed the wrong gender!</b>\nEnter your gender:", parse_mode = "html", reply_markup=markup)
        bot.register_next_step_handler(message, add_gender)


def add_name(message):
    # checking word on correct form
    name = message.text.strip().capitalize()

    if not name.isalpha() or not db_req.does_name_exists(name):
        message = bot.send_message(message.chat.id, "<b>You have typed an incorrect name!</b>\nEnter your name:", parse_mode="html")
        bot.register_next_step_handler(message, add_name)
        return
    else:
        db_req.add_data_to_blank("name", name)
        print("Name has already added!")
        message = bot.send_message(message.chat.id, "Enter your age:")
        bot.register_next_step_handler(message, add_age)


def add_age(message):
    try:
        age = int(message.text.strip())
        if age <= 10 or age >= 100:
            raise Exception
    except Exception:
        message = bot.send_message(message.chat.id, "<b>You have typed an incorrect age!</b>\nEnter your age:",
                                   parse_mode="html")
        bot.register_next_step_handler(message, add_age)
        return

    db_req.add_data_to_blank("age", int(message.text))
    print("Age has already added!")

    message = bot.send_message(message.chat.id, "Enter your city:")
    bot.register_next_step_handler(message, add_city)


def add_city(message):
    city = message.text.strip().capitalize()
    if not city.isalpha() or not db_req.does_city_exists(city):
        message = bot.send_message(message.chat.id, "<b>You have typed an incorrect cityname!</b>\nEnter your city:",
                                   parse_mode="html")
        bot.register_next_step_handler(message, add_city)
        return

    db_req.add_data_to_blank("city", message.text)
    print("City has already added!")

    # for the next step
    message = bot.send_message(message.chat.id, "Enter your description:")
    bot.register_next_step_handler(message, add_description)

def add_description(message):
    # checking
    description = message.text.strip()
    if "http" in description or "www." in description:
        message = bot.send_message(message.chat.id,
                                   "<b>Your description contains links to other resources, It is forbade!!!</b>"
                                   "\nEnter correct description:",
                                   parse_mode="html")
        bot.register_next_step_handler(message, add_description)
        return
    elif re.search(r'\b\w+\.\w+\b', description):
        for tld in db_req.get_all_tlds():
            tld = tld[0]
            if tld in description:
                message = bot.send_message(message.chat.id,
                                           "<b>Your description contains links to other resources, It is forbade!!!</b>"
                                           "\nEnter correct description:",
                                           parse_mode="html")
                bot.register_next_step_handler(message, add_description)
                return

    db_req.add_data_to_blank("description", message.text)
    print("Description has already added!")
    # for the next step
    message = bot.send_message(message.chat.id, "Enter your photo:")
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
