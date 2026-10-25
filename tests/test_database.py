"""Тесты слоя базы данных SQLite (ПР7).

Каждый тест работает с отдельной временной базой, поэтому
рабочая база data/tripplanner.sqlite не изменяется.
"""

import json
import sqlite3

import pytest

from db import import_json
from db.database import get_connection


@pytest.fixture
def db_path(tmp_path):
    """Временная база, заполненная данными из JSON-файлов проекта."""
    path = tmp_path / "test.sqlite"
    import_json.main(path)
    return path


def count_json(filename):
    with open(filename, encoding="utf-8") as file:
        return len(json.load(file))


def test_tables_created(db_path):
    conn = get_connection(db_path)
    tables = {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    conn.close()
    assert {"employees", "routes", "trips"} <= tables


def test_import_matches_json(db_path):
    conn = get_connection(db_path)
    for table, filename in [
        ("employees", import_json.EMPLOYEES_FILE),
        ("routes", import_json.ROUTES_FILE),
        ("trips", import_json.TRIPS_FILE),
    ]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert count == count_json(filename)
    conn.close()


def test_import_can_be_repeated(db_path):
    import_json.main(db_path)
    conn = get_connection(db_path)
    count = conn.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
    conn.close()
    assert count == count_json(import_json.TRIPS_FILE)


def test_is_cancelled_stored_as_integer(db_path):
    conn = get_connection(db_path)
    values = {
        row[0] for row in conn.execute("SELECT is_cancelled FROM trips")
    }
    conn.close()
    assert values <= {0, 1}


def test_foreign_key_is_checked(db_path):
    conn = get_connection(db_path)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO trips (employee_id, route_id, start_date, "
            "end_date, budget_limit) VALUES (?, ?, ?, ?, ?)",
            [999, 1, "2026-12-01", "2026-12-02", 1000],
        )
    conn.close()


def test_join_returns_related_names(db_path):
    conn = get_connection(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT employees.name AS employee_name, routes.destination
        FROM trips
        JOIN employees ON trips.employee_id = employees.id
        JOIN routes ON trips.route_id = routes.id
        WHERE trips.id = ?
        """,
        [1],
    ).fetchone()
    conn.close()
    assert row["employee_name"] == "Иванова Мария Сергеевна"
    assert row["destination"] == "Санкт-Петербург"
