"""Автоматизированные тесты функций работы с командировками."""

from datetime import date

import pytest

from trips import (
    calculate_trip_duration,
    cancel_trip,
    check_budget_status,
    create_trip,
    is_employee_traveling,
)


def test_calculate_trip_duration():
    start = date(2026, 10, 5)
    end = date(2026, 10, 10)
    assert calculate_trip_duration(start, end) == 5


def test_check_budget_status_within_limit():
    assert check_budget_status(42500, 50000) == "Расходы в пределах бюджета"


def test_check_budget_status_exceeded():
    assert check_budget_status(60000, 50000) == "Бюджет превышен"


def test_is_employee_traveling_false_for_empty_list():
    assert not is_employee_traveling([], 1, date(2026, 10, 5))


def test_create_trip_adds_trip():
    trips = []
    trip = create_trip(
        trips, 1, 1, date(2026, 11, 1), date(2026, 11, 5), 30000
    )
    assert len(trips) == 1
    assert trip["status"] == "запланирована"


def test_create_trip_forbids_overlap():
    trips = []
    create_trip(
        trips, 1, 1, date(2026, 11, 1), date(2026, 11, 5), 30000
    )
    with pytest.raises(ValueError):
        create_trip(
            trips, 1, 2, date(2026, 11, 3), date(2026, 11, 7), 20000
        )


def test_cancel_trip():
    trips = []
    trip = create_trip(
        trips, 1, 1, date(2026, 11, 1), date(2026, 11, 5), 30000
    )
    assert cancel_trip(trips, trip["id"]) is True
    assert trips[0]["status"] == "отменена"
