from configparser import ConfigParser

config = ConfigParser()


def get_token():
    try:
        file = open("settings.ini", "x")
    except:
        pass

    config.read("settings.ini")
    try:
        token = config["SETTINGS"]["TOKEN"]
    except:
        token = input("Введите токен вашего бота: ")
        if not "SETTINGS" in config:
            config.add_section("SETTINGS")
        config.set("SETTINGS", "TOKEN", token)
        with open("settings.ini", "w") as configfile:
            config.write(configfile)

    return token


def check_main_chat_id():
    try:
        file = open("settings.ini", "x")
    except:
        pass

    config.read("settings.ini")
    try:
        main_chat_id = config["SETTINGS"]["main_chat_id"]
    except:
        main_chat_id = None

    return main_chat_id is not None


def set_main_chat_id(main_chat_id):
    try:
        file = open("settings.ini", "x")
    except:
        pass

    config.read("settings.ini")
    config.set("SETTINGS", "main_chat_id", main_chat_id)
    with open("settings.ini", "w") as configfile:
        config.write(configfile)


def get_main_chat_id():
    config.read("settings.ini")
    return config["SETTINGS"]["main_chat_id"]
