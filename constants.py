LANGUAGES = {
    'english' : 0,
    'ukrainian' : 1
}

USER_LANG = 0 # english language (default)

MESS_WELCOME = "MESS_WELCOME"

MESS_ENTER_LANG = "BUT_SET_LANG"
MESS_EX_ENTER_LANG_INCORRECT_LANG = "MESS_EX_SET_LANG_INCORRECT_LANG"

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

MESS_EX_EXPECT_TEXT = "MESS_EX_EXPECT_TEXT"
MESS_EX_EXPECT_PHOTO = "MESS_EX_EXPECT_PHOTO"

MESS_BLANK_ALMOST_READY = "MESS_BLANK_ALMOST_READY"
MESS_ENTER_GENDER_TO_SEARCH = "MESS_ENTER_GENDER_TO_SEARCH"

MESS_ENTER_MIN_AGE_TO_SEARCH = "MESS_ENTER_MIN_AGE_TO_SEARCH"

MESS_ENTER_MAX_AGE_TO_SEARCH = "MESS_ENTER_MAX_AGE_TO_SEARCH"

MESS_LETS_SEARCH = "MESS_LETS_SEARCH"

MESS_DIDNT_PUBLISHED = "MESS_DIDNT_PUBLISHED"

BUT_CREATE_NEW_BLANK = "BUT_CREATE_NEW_BLANK"
BUT_MALE = "BUT_MALE"
BUT_FEMALE = "BUT_FEMALE"
BUT_PUBLISH_AND_SEARCH = "BUT_PUBLISH_AND_SEARCH"

DB_COL_LANG = 'language'
DB_COL_GENDER = 'gender'
DB_COL_NAME = 'name'
DB_COL_AGE = 'age'
DB_COL_CITY = 'city'
DB_COL_DESC = 'description'
DB_COL_PREF_GENDER = 'preferences_gender'
DB_COL_PREF_MIN_AGE_TO_SEE = 'preferances_to_see_min_age'
DB_COL_PREF_MAX_AGE_TO_SEE = 'preferances_to_see_max_age'
DB_COL_PREF_MIN_AGE_OTHER_TO_SEE_ME = 'preferances_other_to_see_min_age'
DB_COL_PREF_MAX_AGE_OTHER_TO_SEE_ME = 'preferances_other_to_see_max_age'


GENDER_MALE = 'm'
GENDER_FEMALE = 'f'


MESSAGES = {
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
    MESS_ENTER_LANG: (
        "Choose your language: 🌎",
        "Виберіть свою мову: 🌎"
    ),
    MESS_EX_ENTER_LANG_INCORRECT_LANG : (
        "<b>You have typed incorrect language ❌</b>\nEnter your language: 🌎",
        "<b>Ви ввели неправильну мову ❌</b>\nВведіть вашу мову: 🌎"
    ),

    MESS_BLANK_ALMOST_READY : (
        "Your blank is almost ready! Here it is!",
        "Твій бланк майже готовий! Ось він!"
    ),

    MESS_ENTER_GENDER_TO_SEARCH : (
        "Enter genser to search!",
        "Введіть стать для пошуку"
    ),

    MESS_ENTER_MIN_AGE_TO_SEARCH : (
        "Enter MIN age of blanks to see",
        "Введіть мінімальний вік для пошуку"
    ),

    MESS_ENTER_MAX_AGE_TO_SEARCH : (
        "Enter MAX age of blanks to see",
        "Введіть максимальний вік для пошуку"
    ),

    MESS_LETS_SEARCH : (
        "OKEY, that is all! Let's watch the blanks!!!",
        "ОКЕЙ, це все! Давай диитися анкети!!!"
    ),

    MESS_DIDNT_PUBLISHED : (
        "You didn't publish tour blank, you can't search other blanks\nPublish my blank and START searching!",
        "Ви не опублікували ваш бланк, тому ви не можете дивитися інші анкети\nОпублікувати мій бланк та почати пошук!"
    ),

    MESS_EX_EXPECT_TEXT : (
        "<b>You  have typed not a text ❌</b>\nEnter text: 🌎",
        "<b>Ви ввели не текст ❌</b>\nВведіть текст: 🌎"
    ),

    MESS_EX_EXPECT_PHOTO : (
        "<b>You  have typed not a photo ❌</b>\nEnter yout photo: 📸",
        "<b>Ви ввели не фото ❌</b>\nВведіть ваше фото: 📸"
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
    ),
    BUT_PUBLISH_AND_SEARCH : (
        "Publish my blank and START searching!",
        "Опублікувати мій бланк та почати пошук!"
    )
}

EXCEPTIONS = {
    'text' : MESS_EX_EXPECT_TEXT,
    'photo' : MESS_EX_EXPECT_PHOTO
}
