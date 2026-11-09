"""Перенос данных из базы ПР7 (sqlite3) в базу Django через ORM.

Исходная база data/tripplanner.sqlite остаётся без изменений и
используется как источник. Записи создаются средствами Django ORM
в целевой базе, указанной в настройках DATABASES (db.sqlite3).

Запуск из корневого каталога проекта:
    python db/import_sqlite_to_orm.py
"""
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
from django.db import transaction

# Корневой каталог проекта: скрипт лежит в подкаталоге db.
BASE_DIR = Path(__file__).resolve().parent.parent

# Добавляем корень проекта в пути поиска модулей Python.
sys.path.insert(0, str(BASE_DIR))

# Путь к исходной базе данных ПР7.
SOURCE_DB = BASE_DIR / "data" / "tripplanner.sqlite"

# Модуль настроек Django и инициализация.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripplanner.settings")
django.setup()

# Модели импортируются только после инициализации Django.
from employees.models import Employee  # noqa: E402
from trips.models import Route, Trip  # noqa: E402


def main():
    """Прочитать исходную базу и перенести данные через ORM."""
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Исходная база не найдена: {SOURCE_DB}")

    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row

        employees = connection.execute(
            "SELECT id, name, position FROM employees ORDER BY id"
        ).fetchall()
        routes = connection.execute(
            "SELECT id, origin, destination, transport "
            "FROM routes ORDER BY id"
        ).fetchall()
        trips = connection.execute(
            "SELECT id, employee_id, route_id, start_date, end_date, "
            "budget_limit, expenses, is_cancelled FROM trips ORDER BY id"
        ).fetchall()

        # Запись одной транзакцией: при ошибке изменения откатываются.
        with transaction.atomic():
            # Сначала независимые сущности.
            for row in employees:
                Employee.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "name": row["name"],
                        "position": row["position"],
                    },
                )
            for row in routes:
                Route.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "origin": row["origin"],
                        "destination": row["destination"],
                        "transport": row["transport"],
                    },
                )
            # Затем командировки, ссылающиеся на них внешними ключами.
            for row in trips:
                Trip.objects.update_or_create(
                    pk=row["id"],
                    defaults={
                        "employee_id": row["employee_id"],
                        "route_id": row["route_id"],
                        "start_date": date.fromisoformat(row["start_date"]),
                        "end_date": date.fromisoformat(row["end_date"]),
                        "budget_limit": row["budget_limit"],
                        "expenses": row["expenses"],
                        "is_cancelled": bool(row["is_cancelled"]),
                    },
                )

    print("Перенос данных завершён.")
    print(f"Сотрудников: {Employee.objects.count()}")
    print(f"Маршрутов: {Route.objects.count()}")
    print(f"Командировок: {Trip.objects.count()}")


if __name__ == "__main__":
    main()
