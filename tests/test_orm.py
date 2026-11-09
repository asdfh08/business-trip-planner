"""Тесты моделей Django и операций ORM (ПР9).

Тесты работают с базой данных проекта (db.sqlite3), заполненной
при переносе данных из базы ПР7, и проверяют модели, связи и
основные ORM-запросы.
"""
import os
from datetime import date

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripplanner.settings")
django.setup()

from django.test.utils import setup_test_environment  # noqa: E402

try:
    setup_test_environment()
except RuntimeError:
    pass

from employees.models import Employee  # noqa: E402
from trips.models import Route, Trip  # noqa: E402


def test_record_counts():
    assert Employee.objects.count() == 3
    assert Route.objects.count() == 3
    assert Trip.objects.count() == 5


def test_foreign_keys_resolve_related_objects():
    trip = Trip.objects.select_related("employee", "route").get(pk=1)
    assert trip.employee.name == "Иванова Мария Сергеевна"
    assert trip.route.destination == "Санкт-Петербург"


def test_related_name_reverse_access():
    employee = Employee.objects.get(pk=1)
    assert employee.trips.count() == 3


def test_filter_active_trips():
    active = Trip.objects.filter(is_cancelled=False)
    assert active.count() == 4


def test_duration_property():
    trip = Trip.objects.get(pk=1)
    assert trip.duration == 9


def test_budget_status_property():
    exceeded = Trip.objects.get(pk=5)
    assert exceeded.budget_status == "Бюджет превышен"
    not_entered = Trip.objects.get(pk=2)
    assert not_entered.budget_status == "Расходы ещё не внесены"


def test_date_field_is_date_object():
    trip = Trip.objects.get(pk=1)
    assert isinstance(trip.start_date, date)
