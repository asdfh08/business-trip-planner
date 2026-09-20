"""Функции для работы с командировками — списком trips."""
from datetime import date
from typing import Iterator

from employees import get_employee


def calculate_trip_duration(start_date: date, end_date: date) -> int:
    """Возвращает продолжительность командировки в днях (функция ПР1)."""
    duration = (end_date - start_date).days
    return duration


def check_budget_status(expenses: float, limit: float) -> str:
    """Сравнивает расходы с лимитом бюджета (функция ПР1)."""
    if expenses > limit:
        return "Бюджет превышен"
    elif expenses == limit:
        return "Бюджет использован полностью"
    else:
        return "Расходы в пределах бюджета"


def get_trip_summary(employees: dict[int, dict], trip: dict) -> str:
    """Формирует краткую сводку по командировке (развитие функции ПР1)."""
    employee = get_employee(employees, trip["employee_id"])
    name = employee["name"] if employee else "Неизвестный сотрудник"
    duration = calculate_trip_duration(trip["start_date"], trip["end_date"])
    return (
        f"Сотрудник {name} отправляется в командировку "
        f"в город {trip['destination']} на {duration} дн."
    )


def is_employee_traveling(
    trips: list[dict], employee_id: int, check_date: date
) -> bool:
    """Проверить, находится ли сотрудник в другой командировке на дату."""
    for trip in trips:
        if trip["employee_id"] != employee_id:
            continue
        if trip["status"] == "отменена":
            continue
        if trip["start_date"] <= check_date <= trip["end_date"]:
            return True
    return False


def create_trip(
    trips: list[dict],
    employee_id: int,
    destination: str,
    start_date: date,
    end_date: date,
    budget_limit: float,
) -> dict:
    """Создать новую командировку и добавить её в список trips.

    Вызывает исключение ValueError, если сотрудник уже находится
    в командировке в указанный период.
    """
    if is_employee_traveling(trips, employee_id, start_date) or \
            is_employee_traveling(trips, employee_id, end_date):
        raise ValueError(
            "Сотрудник уже находится в другой командировке в этот период"
        )
    new_id = max((trip["id"] for trip in trips), default=0) + 1
    trip = {
        "id": new_id,
        "employee_id": employee_id,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget_limit": budget_limit,
        "expenses": None,
        "status": "запланирована",
    }
    trips.append(trip)
    return trip


def cancel_trip(trips: list[dict], trip_id: int) -> bool:
    """Отменить командировку по идентификатору.

    Возвращает True, если командировка найдена и отменена,
    иначе — False.
    """
    for trip in trips:
        if trip["id"] == trip_id:
            trip["status"] = "отменена"
            return True
    return False


def filter_trips_by_status(trips: list[dict], status: str) -> list[dict]:
    """Отобрать командировки с указанным статусом."""
    return [trip for trip in trips if trip["status"] == status]


def sort_trips_by_date(trips: list[dict]) -> list[dict]:
    """Вернуть командировки, отсортированные по дате начала."""
    return sorted(trips, key=lambda trip: trip["start_date"])


def filter_expensive_trips(
    trips: list[dict], threshold: float
) -> Iterator[dict]:
    """Вернуть генератор командировок с расходами выше порога threshold."""
    return (
        trip for trip in trips
        if trip["expenses"] is not None and trip["expenses"] > threshold
    )


def get_total_expenses(trips: list[dict]) -> float:
    """Вернуть суммарные расходы по всем командировкам."""
    total = 0.0
    for trip in trips:
        if trip["expenses"] is not None:
            total += trip["expenses"]
    return total


def get_statistics(trips: list[dict]) -> dict:
    """Собрать краткую статистику по командировкам."""
    active_trips = filter_trips_by_status(trips, "запланирована")
    return {
        "total_trips": len(trips),
        "active_trips": len(active_trips),
        "cancelled_trips": len(filter_trips_by_status(trips, "отменена")),
        "total_expenses": get_total_expenses(trips),
    }
