"""Перенос данных проекта из JSON-файлов в базу SQLite.

Запуск из корня проекта:
    python -m db.import_json

Порядок импорта важен: сначала сотрудники и маршруты, затем
командировки, которые ссылаются на них внешними ключами.
Перед импортом таблицы очищаются, поэтому скрипт можно запускать
повторно - дубликатов и ошибок уникальности не будет.
"""

import json

from db.database import BASE_DIR, DB_PATH, create_schema, get_connection

EMPLOYEES_FILE = BASE_DIR / "data" / "employees.json"
ROUTES_FILE = BASE_DIR / "data" / "routes.json"
TRIPS_FILE = BASE_DIR / "data" / "trips.json"


def load_json(filename):
    """Прочитать список записей из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn):
    """Удалить старые записи: сначала зависимую таблицу trips."""
    conn.execute("DELETE FROM trips")
    conn.execute("DELETE FROM routes")
    conn.execute("DELETE FROM employees")


def import_employees(conn):
    """Перенести сотрудников в таблицу employees."""
    employees = load_json(EMPLOYEES_FILE)
    conn.executemany(
        """
        INSERT INTO employees (id, name, position)
        VALUES (?, ?, ?)
        """,
        [
            (employee["id"], employee["name"], employee["position"])
            for employee in employees
        ],
    )


def import_routes(conn):
    """Перенести маршруты в таблицу routes."""
    routes = load_json(ROUTES_FILE)
    conn.executemany(
        """
        INSERT INTO routes (id, origin, destination, transport)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                route["id"],
                route["origin"],
                route["destination"],
                route["transport"],
            )
            for route in routes
        ],
    )


def import_trips(conn):
    """Перенести командировки в таблицу trips.

    Логическое значение is_cancelled из JSON (true/false)
    приводится к целому числу 1/0, которое хранится в SQLite.
    Значение null в expenses становится NULL.
    """
    trips = load_json(TRIPS_FILE)
    conn.executemany(
        """
        INSERT INTO trips (
            id, employee_id, route_id, start_date, end_date,
            budget_limit, expenses, is_cancelled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                trip["id"],
                trip["employee_id"],
                trip["route_id"],
                trip["start_date"],
                trip["end_date"],
                trip["budget_limit"],
                trip["expenses"],
                int(trip["is_cancelled"]),
            )
            for trip in trips
        ],
    )


def main(db_path=DB_PATH):
    """Создать таблицы и перенести в них все данные из JSON."""
    conn = get_connection(db_path)
    try:
        create_schema(conn)
        clear_tables(conn)
        import_employees(conn)
        import_routes(conn)
        import_trips(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
