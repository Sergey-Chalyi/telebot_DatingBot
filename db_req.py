import pickle
import sqlite3

cur_user_tg_id = None

DB_NAME = "DB_USERS_BOT_DATING.db"

req_is_user_exists_in_db = """SELECT tg_id 
                        FROM USERS_GENERAL_INFO
                        WHERE tg_id = (?)"""

req_add_user_to_db = """INSERT INTO USERS_GENERAL_INFO (tg_id, tg_message_obj)
                    VALUES (?, ?)"""


req_add_other_info_to_blank = """UPDATE USERS_GENERAL_INFO
                                SET {column_name} = (?)
                                WHERE tg_id = (?)"""

req_get_user_blank_info = """SELECT photo, name, age, city, description
                            FROM USERS_GENERAL_INFO
                            WHERE tg_id = (?)
                          """

req_get_name = """SELECT name FROM PEOPLE_NAMES WHERE name = (?)"""

req_get_city = """SELECT city FROM COUNTRIES_AND_CITIES WHERE city = (?)"""

req_get_all_tlds = """SELECT tld FROM TLDS"""

req_get_user_lang = """SELECT language FROM USERS_GENERAL_INFO WHERE tg_id = (?)"""

req_get_user_info_for_searching = """SELECT tg_id, photo, name, age, city, description 
                                    FROM USERS_GENERAL_INFO 
                                    WHERE tg_id != (?) AND gender = (?) AND (age >= (?) AND age <= (?))"""

req_get_user_info = """SELECT {column_name} FROM USERS_GENERAL_INFO WHERE tg_id = (?)"""

req_get_users_likes = """SELECT tg_id_blank FROM LIKES WHERE tg_id_user = (?)"""

req_add_users_likes = """INSERT INTO LIKES (tg_id_user, tg_id_blank, like) VALUES (?, ?, ?)"""

def db_is_user_exists(user_tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        if DB.execute(req_is_user_exists_in_db, (user_tg_id,)).fetchone() is None:
            return False
        else:
            return True

def db_add_user(user_tg_id, message):
    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_user_to_db, (user_tg_id, pickle.dumps(message)))
        DB.commit()
# def db_add_gender_to_blank(id ,gender):
#     with sqlite3.connect(DB_NAME) as DB:
#         DB.execute(req_add_gender_to_blank, (id, gender))

def db_add_data_to_blank(cur_user_tg_id, column_name, value):
    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_other_info_to_blank.format(column_name = column_name), (value, cur_user_tg_id))
        DB.commit()


def db_get_user_blank_info(tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        return DB.execute(req_get_user_blank_info, (tg_id,)).fetchone()


def db_does_name_exists(name):
    with sqlite3.connect(DB_NAME) as db:
        return False if db.execute(req_get_name, (name,)).fetchone() is None else True


def db_does_city_exists(city):
    with sqlite3.connect(DB_NAME) as db:
        return False if db.execute(req_get_city, (city,)).fetchone() is None else True



def db_get_all_tlds():
    with sqlite3.connect(DB_NAME) as db:
        return db.execute(req_get_all_tlds).fetchall()


def db_get_user_lang(tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        return DB.execute(req_get_user_lang, (tg_id,)).fetchone()[0]

def db_get_user_info_for_searching(tg_id, gender, min_age, max_age):
    with sqlite3.connect(DB_NAME) as DB:
        list_info = []
        cursor = DB.execute(req_get_user_info_for_searching, (tg_id, gender, min_age, max_age))
        for el in cursor:
            list_info.append(el)
        return list_info


def db_get_user_info(col_name, tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        return DB.execute(req_get_user_info.format(column_name=col_name), (tg_id,)).fetchone()[0]

def db_get_users_likes(tg_id_user):
    with sqlite3.connect(DB_NAME) as DB:
        likes_list = []
        cursor = DB.execute(req_get_users_likes, (tg_id_user,))
        for el in cursor:
            likes_list.append(el[0])
        return likes_list

def db_add_users_likes(tg_id_user, tg_id_blank, like):
    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_users_likes, (tg_id_user, tg_id_blank, like))
        DB.commit()
