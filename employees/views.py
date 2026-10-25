"""Представления приложения employees.

Данные читаются из базы SQLite. Значения от пользователя и из URL
передаются в запросы только параметрами ?, без подстановки в строку.
"""
import sqlite3
from datetime import date

from django.shortcuts import render

from db.database import get_connection

EMPLOYEES_SQL = """
    SELECT id, name, position
    FROM employees
    ORDER BY name
"""

EMPLOYEE_SQL = """
    SELECT id, name, position
    FROM employees
    WHERE id = ?
"""

EMPLOYEE_TRIPS_SQL = """
    SELECT
        trips.id,
        strftime('%d.%m.%Y', trips.start_date) AS start_date,
        strftime('%d.%m.%Y', trips.end_date) AS end_date,
        trips.is_cancelled,
        routes.origin,
        routes.destination
    FROM trips
    JOIN routes ON trips.route_id = routes.id
    WHERE trips.employee_id = ?
    ORDER BY trips.start_date
"""

EMPLOYEE_TRAVELING_SQL = """
    SELECT COUNT(*) AS active_trips
    FROM trips
    WHERE employee_id = ?
        AND is_cancelled = 0
        AND start_date <= ?
        AND end_date >= ?
"""

AVAILABLE_EMPLOYEES_SQL = """
    SELECT
        employees.id,
        employees.name,
        employees.position
    FROM employees
    WHERE employees.id NOT IN (
        SELECT trips.employee_id
        FROM trips
        WHERE trips.is_cancelled = 0
            AND trips.start_date <= ?
            AND trips.end_date >= ?
    )
    ORDER BY employees.name
"""


def employees(request):
    """Список сотрудников."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    employees_list = conn.execute(EMPLOYEES_SQL).fetchall()
    conn.close()
    context = {"employees": employees_list}
    return render(request, "employees/employee_list.html", context)


def employee_detail(request, employee_id):
    """Карточка сотрудника: данные, статус на сегодня, командировки."""
    today = date.today().isoformat()
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    employee = conn.execute(EMPLOYEE_SQL, [employee_id]).fetchone()
    trips = []
    traveling = False
    if employee is not None:
        trips = conn.execute(EMPLOYEE_TRIPS_SQL, [employee_id]).fetchall()
        result = conn.execute(
            EMPLOYEE_TRAVELING_SQL, [employee_id, today, today]
        ).fetchone()
        traveling = result["active_trips"] > 0
    conn.close()
    context = {"employee": employee, "trips": trips, "traveling": traveling}
    return render(
        request, "employees/employee_detail.html", context,
        status=404 if employee is None else 200,
    )


def available_employees(request):
    """Поиск сотрудников, свободных от командировок на выбранную дату."""
    selected_date = request.GET.get("date", "")
    employees_list = []
    error = None
    if selected_date:
        try:
            date.fromisoformat(selected_date)
        except ValueError:
            error = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            employees_list = conn.execute(
                AVAILABLE_EMPLOYEES_SQL, [selected_date, selected_date]
            ).fetchall()
            conn.close()
    context = {
        "employees": employees_list,
        "selected_date": selected_date,
        "error": error,
    }
    return render(request, "employees/available.html", context)
