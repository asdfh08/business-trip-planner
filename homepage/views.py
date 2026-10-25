"""Представления приложения homepage."""
import sqlite3

from django.shortcuts import render

from db.database import get_connection

SUMMARY_SQL = """
    SELECT
        (SELECT COUNT(*) FROM employees) AS employees_count,
        (SELECT COUNT(*) FROM trips WHERE is_cancelled = 0)
            AS active_trips_count
"""


def index(request):
    """Главная страница сервиса со сводкой из базы данных."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    summary = conn.execute(SUMMARY_SQL).fetchone()
    conn.close()
    return render(request, "homepage/index.html", {"summary": summary})


def page_not_found(request, exception):
    """Собственная страница 404."""
    return render(request, "404.html", status=404)
