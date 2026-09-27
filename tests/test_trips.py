"""Тесты класса Trip и функций работы с командировками."""

from datetime import date

import pytest

from models import Employee, Route, Trip
from models.trips import (
    cancel_trip,
    check_budget_status,
    create_trip,
    is_employee_traveling,
    sort_trips_by_date,
)


def make_employee() -> Employee:
    return Employee(1, "Иванова Мария", "Менеджер")


def make_route() -> Route:
    return Route(1, "Москва", "Казань", "Поезд")


def test_trip_creation_links_objects():
    employee = make_employee()
    route = make_route()
    trip = Trip(
        1, employee, route, date(2026, 10, 5), date(2026, 10, 10), 50000
    )
    assert trip.id == 1
    assert trip.employee is employee
    assert trip.route is route
    assert trip.is_cancelled is False
    assert trip.expenses is None


def test_trip_duration():
    trip = Trip(
        1, make_employee(), make_route(),
        date(2026, 10, 5), date(2026, 10, 10), 50000,
    )
    assert trip.duration() == 5


def test_trip_str_contains_route_and_employee():
    trip = Trip(
        1, make_employee(), make_route(),
        date(2026, 10, 5), date(2026, 10, 10), 50000,
    )
    text = str(trip)
    assert "Иванова Мария" in text
    assert "Москва → Казань" in text
    assert "запланирована" in text


def test_trip_cancel():
    trip = Trip(
        1, make_employee(), make_route(),
        date(2026, 10, 5), date(2026, 10, 10), 50000,
    )
    trip.cancel()
    assert trip.is_cancelled


def test_trip_budget_status():
    trip = Trip(
        1, make_employee(), make_route(),
        date(2026, 10, 5), date(2026, 10, 10), 50000,
    )
    trip.set_expenses(42500)
    assert trip.get_budget_status() == "Расходы в пределах бюджета"


def test_check_budget_status_exceeded():
    assert check_budget_status(60000, 50000) == "Бюджет превышен"


def test_trip_invalid_dates_raise_error():
    with pytest.raises(ValueError):
        Trip(
            1, make_employee(), make_route(),
            date(2026, 10, 10), date(2026, 10, 5), 50000,
        )


def test_validate_dates_static_method():
    assert Trip.validate_dates(date(2026, 10, 5), date(2026, 10, 10))
    assert not Trip.validate_dates(date(2026, 10, 10), date(2026, 10, 5))


def test_create_trip_adds_trip():
    trips = []
    trip = create_trip(
        trips, make_employee(), make_route(),
        date(2026, 11, 1), date(2026, 11, 5), 30000,
    )
    assert trip is not None
    assert trips == [trip]


def test_create_trip_forbids_overlap():
    trips = []
    employee = make_employee()
    route = make_route()
    create_trip(
        trips, employee, route, date(2026, 11, 1), date(2026, 11, 5), 30000
    )
    second = create_trip(
        trips, employee, route, date(2026, 11, 3), date(2026, 11, 7), 20000
    )
    assert second is None
    assert len(trips) == 1


def test_cancelled_trip_does_not_block_employee():
    trips = []
    employee = make_employee()
    route = make_route()
    first = create_trip(
        trips, employee, route, date(2026, 11, 1), date(2026, 11, 5), 30000
    )
    first.cancel()
    second = create_trip(
        trips, employee, route, date(2026, 11, 3), date(2026, 11, 7), 20000
    )
    assert second is not None
    assert len(trips) == 2


def test_is_employee_traveling_false_for_empty_list():
    assert not is_employee_traveling(
        [], make_employee(), date(2026, 10, 5), date(2026, 10, 6)
    )


def test_cancel_trip():
    trips = []
    trip = create_trip(
        trips, make_employee(), make_route(),
        date(2026, 11, 1), date(2026, 11, 5), 30000,
    )
    assert cancel_trip(trips, trip.id) is True
    assert trips[0].is_cancelled
    assert cancel_trip(trips, 99) is False


def test_sort_trips_by_date():
    employee = make_employee()
    route = make_route()
    late = Trip(1, employee, route, date(2026, 12, 1), date(2026, 12, 2), 1)
    early = Trip(2, employee, route, date(2026, 10, 1), date(2026, 10, 2), 1)
    assert sort_trips_by_date([late, early]) == [early, late]
