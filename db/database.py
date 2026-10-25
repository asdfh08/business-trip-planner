"""Подключение к базе данных SQLite.

Путь к базе строится от корня проекта, поэтому подключение работает
одинаково при запуске сервера Django, скрипта импорта и тестов.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tripplanner.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection(db_path=DB_PATH):
    """Открыть соединение с базой и включить проверку внешних ключей.

    По умолчанию SQLite не проверяет, что внешний ключ ссылается
    на существующую запись, поэтому PRAGMA выполняется при каждом
    подключении.
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn):
    """Создать таблицы по командам из sql/schema.sql."""
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
