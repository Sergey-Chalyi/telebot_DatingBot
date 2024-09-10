import pickle
import sqlite3

cur_user_tg_id = None

DB_NAME = "DB_USERS_BOT_DATING.db"

req_is_user_exists_in_priv_tab = """SELECT tg_id 
                        FROM USERS_PRIVATE_INFO
                        WHERE tg_id = (?)"""

req_add_user_to_priv_tab = """INSERT INTO USERS_PRIVATE_INFO (tg_id, message)
                    VALUES (?, ?)"""

req_add_gender_to_blank = """INSERT INTO USERS_GENERAL_INFO (gender)
                            VALUES (?)"""

req_add_other_info_to_blank = """UPDATE USERS_GENERAL_INFO
                                SET {column_name} = (?)
                                WHERE id = (
                                    SELECT id 
                                    FROM USERS_PRIVATE_INFO
                                    WHERE tg_id = (?)
                                )"""

req_get_user_blank_info = """SELECT photo, name, age, city, description
                            FROM USERS_GENERAL_INFO
                            WHERE id = (SELECT id 
                                FROM USERS_PRIVATE_INFO
                                WHERE tg_id = (?)
                            )"""

req_get_uk_name = """SELECT name FROM UK_NAMES WHERE name = (?)"""

req_get_eng_name = """SELECT name FROM ENG_NAMES WHERE name = (?)"""

req_get_uk_city = """SELECT name FROM UK_CITIES WHERE name = (?)"""

req_get_eng_city = """SELECT city FROM ENG_CITIES WHERE city = (?)"""

req_get_all_tlds = """SELECT name FROM TLDS"""

def is_user_exists_in_priv_db(user_tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        if DB.execute(req_is_user_exists_in_priv_tab, (user_tg_id,)).fetchone() is None:
            return False
        else:
            return True

def add_user_to_priv_db(user_tg_id, message):
    global cur_user_tg_id
    cur_user_tg_id = user_tg_id

    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_user_to_priv_tab, (user_tg_id, pickle.dumps(message)))

def add_gender_to_blank(gender):
    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_gender_to_blank, (gender,))

def add_data_to_blank(column_name, value):
    global cur_user_tg_id
    with sqlite3.connect(DB_NAME) as DB:
        DB.execute(req_add_other_info_to_blank.format(column_name = column_name), (value, cur_user_tg_id))

def get_user_blank_info(tg_id):
    with sqlite3.connect(DB_NAME) as DB:
        return DB.execute(req_get_user_blank_info, (tg_id,)).fetchone()


def does_name_exists(name):
    with sqlite3.connect(DB_NAME) as db:
        if db.execute(req_get_uk_name, (name,)).fetchone() is None:
            if db.execute(req_get_eng_name, (name,)).fetchone() is None:
                return False
            else:
                return True
        else:
            return True


def does_city_exists(city):
    with sqlite3.connect(DB_NAME) as db:
        if db.execute(req_get_uk_city, (city,)).fetchone() is None:
            if db.execute(req_get_eng_city, (city,)).fetchone() is None:
                return False
            else:
                return True
        else:
            return True


def get_all_tlds():
    with sqlite3.connect(DB_NAME) as db:
        return db.execute(req_get_all_tlds).fetchall()
