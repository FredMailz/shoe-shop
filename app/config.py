import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.ini"


class ConfigError(Exception):
    pass


def load_database_config(path=CONFIG_PATH):
    parser = configparser.ConfigParser()
    if not parser.read(path, encoding="utf-8"):
        raise ConfigError("Файл config.ini не найден. Скопируйте config.ini.example в config.ini.")
    if "database" not in parser:
        raise ConfigError("В config.ini нет раздела [database].")
    section = parser["database"]
    try:
        return {
            "host": section["host"],
            "port": section["port"],
            "dbname": section["name"],
            "user": section["user"],
            "password": section["password"],
        }
    except KeyError as error:
        raise ConfigError(f"В разделе [database] не задан параметр {error}.") from error
