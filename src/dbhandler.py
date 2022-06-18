import os
import config
import json
from cryptocode import encrypt, decrypt

db_folder = os.path.join("data")
db_path = os.path.join("data", "logins.json")


def write_to_db(login: str, password: str, user_id: str):
    if not os.path.exists(db_folder):
        os.mkdir(db_folder)
    if not os.path.exists(db_path):
        file = open(db_path, "w").close()
    password = encrypt(password=config.SECRET_WORD, message=password)
    file = open(db_path, "r")
    json_file_contents = file.read()
    file.close()
    if json_file_contents != "":
        json_file_contents = json.loads(json_file_contents)
    record = {user_id: {"login": login, "password": password}}
    to_json = []
    if json_file_contents:
        for el in json_file_contents:
            to_json.append(el)
    to_json.append(record)
    file = open(db_path, "w")
    json.dump(to_json, file, indent=2)
    file.close()


def remove_from_db(user_id: str):
    if os.path.exists(db_path):
        file = open(db_path, "r")
        file_contents = file.read()
        file.close()
        if file_contents != "":
            file_contents = json.loads(file_contents)
            for el in file_contents.copy():
                if list(el.keys())[0] == user_id:
                    file_contents.remove(el)
            file = open(db_path, "w+")
            if file_contents:
                json.dump(file_contents, file, indent=2)
            file.close()


def read_from_db(user_id: str):
    user_data = {}
    if os.path.exists(db_path):
        file = open(db_path, "r")
        file_contents = file.read()
        if file_contents != "":
            file_contents = json.loads(file_contents)
            for el in file_contents:
                if list(el.keys())[0] == user_id:
                    user_data = el[user_id]
                    user_data["password"] = decrypt(
                        password=config.SECRET_WORD, enc_dict=user_data["password"]
                    )
                    break
        file.close()
    return user_data
