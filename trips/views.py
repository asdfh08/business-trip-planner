"""Представления приложения trips.

Данные читаются из базы SQLite. Значения от пользователя и из URL
передаются в запросы только параметрами ?, без подстановки в строку.
"""
import sqlite3

from django.shortcuts import render

from db.database import get_connection

TRIPS_SQL = """
    SELECT
        trips.id,
        strftime('%d.%m.%Y', trips.start_date) AS start_date,
        strftime('%d.%m.%Y', trips.end_date) AS end_date,
        trips.is_cancelled,
        employees.name AS employee_name,
        routes.origin,
        routes.destination
    FROM trips
    JOIN employees ON trips.employee_id = employees.id
    JOIN routes ON trips.route_id = routes.id
    ORDER BY trips.start_date
"""

TRIPS_BY_STATUS_SQL = """
    SELECT
        trips.id,
        strftime('%d.%m.%Y', trips.start_date) AS start_date,
        strftime('%d.%m.%Y', trips.end_date) AS end_date,
        trips.is_cancelled,
        employees.name AS employee_name,
        routes.origin,
        routes.destination
    FROM trips
    JOIN employees ON trips.employee_id = employees.id
    JOIN routes ON trips.route_id = routes.id
    WHERE trips.is_cancelled = ?
    ORDER BY trips.start_date
"""

TRIP_SQL = """
    SELECT
        trips.id,
        strftime('%d.%m.%Y', trips.start_date) AS start_date,
        strftime('%d.%m.%Y', trips.end_date) AS end_date,
        CAST(julianday(trips.end_date) - julianday(trips.start_date)
            AS INTEGER) AS duration_days,
        trips.budget_limit,
        trips.expenses,
        trips.is_cancelled,
        CASE
            WHEN trips.expenses IS NULL THEN 'Расходы ещё не внесены'
            WHEN trips.expenses > trips.budget_limit THEN 'Бюджет превышен'
            WHEN trips.expenses = trips.budget_limit
                THEN 'Бюджет использован полностью'
            ELSE 'Расходы в пределах бюджета'
        END AS budget_status,
        employees.id AS employee_id,
        employees.name AS employee_name,
        employees.position AS employee_position,
        routes.origin,
        routes.destination,
        routes.transport
    FROM trips
    JOIN employees ON trips.employee_id = employees.id
    JOIN routes ON trips.route_id = routes.id
    WHERE trips.id = ?
"""

SUMMARY_SQL = """
    SELECT
        COUNT(*) AS total_trips,
        SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active_trips,
        SUM(is_cancelled) AS cancelled_trips,
        SUM(expenses) AS total_expenses,
        AVG(budget_limit) AS avg_budget
    FROM trips
"""

BY_EMPLOYEE_SQL = """
    SELECT
        employees.name AS employee_name,
        COUNT(trips.id) AS trips_count,
        COALESCE(SUM(trips.expenses), 0) AS total_expenses
    FROM employees
    LEFT JOIN trips
        ON employees.id = trips.employee_id
        AND trips.is_cancelled = 0
    GROUP BY employees.id, employees.name
    ORDER BY trips_count DESC, employees.name
"""

BY_ROUTE_SQL = """
    SELECT
        routes.origin,
        routes.destination,
        routes.transport,
        COUNT(trips.id) AS trips_count
    FROM routes
    LEFT JOIN trips
        ON routes.id = trips.route_id
        AND trips.is_cancelled = 0
    GROUP BY routes.id, routes.origin, routes.destination, routes.transport
    ORDER BY trips_count DESC, routes.destination
"""

FREQUENT_TRAVELERS_SQL = """
    SELECT
        employees.name AS employee_name,
        COUNT(trips.id) AS trips_count
    FROM employees
    JOIN trips ON employees.id = trips.employee_id
    WHERE trips.is_cancelled = 0
    GROUP BY employees.id, employees.name
    HAVING COUNT(trips.id) > ?
    ORDER BY trips_count DESC
"""

OVER_BUDGET_SQL = """
    SELECT
        trips.id,
        employees.name AS employee_name,
        routes.destination,
        trips.budget_limit,
        trips.expenses,
        trips.expenses - trips.budget_limit AS overrun
    FROM trips
    JOIN employees ON trips.employee_id = employees.id
    JOIN routes ON trips.route_id = routes.id
    WHERE trips.is_cancelled = 0
        AND trips.expenses > trips.budget_limit
    ORDER BY overrun DESC
"""

# Значение GET-параметра status -> значение поля is_cancelled
STATUS_FILTERS = {"active": 0, "cancelled": 1}


def trips(request):
    """Список командировок с фильтром по статусу (?status=...)."""
    status = request.GET.get("status", "all")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    if status in STATUS_FILTERS:
        trips_list = conn.execute(
            TRIPS_BY_STATUS_SQL, [STATUS_FILTERS[status]]
        ).fetchall()
    else:
        status = "all"
        trips_list = conn.execute(TRIPS_SQL).fetchall()
    conn.close()
    context = {"trips": trips_list, "status": status}
    return render(request, "trips/trip_list.html", context)


def trip_detail(request, trip_id):
    """Карточка командировки со сведениями о сотруднике и маршруте."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    trip = conn.execute(TRIP_SQL, [trip_id]).fetchone()
    conn.close()
    context = {"trip": trip}
    return render(
        request, "trips/trip_detail.html", context,
        status=404 if trip is None else 200,
    )


def statistics(request):
    """Статистика командировок: сводка, группировки, превышения."""
    try:
        min_trips = int(request.GET.get("min_trips", 1))
    except ValueError:
        min_trips = 1
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    context = {
        "summary": conn.execute(SUMMARY_SQL).fetchone(),
        "by_employee": conn.execute(BY_EMPLOYEE_SQL).fetchall(),
        "by_route": conn.execute(BY_ROUTE_SQL).fetchall(),
        "frequent": conn.execute(
            FREQUENT_TRAVELERS_SQL, [min_trips]
        ).fetchall(),
        "over_budget": conn.execute(OVER_BUDGET_SQL).fetchall(),
        "min_trips": min_trips,
    }
    conn.close()
    return render(request, "trips/statistics.html", context)
