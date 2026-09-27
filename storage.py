"""Загрузка и сохранение объектов проекта в JSON-файлы.

JSON остаётся форматом хранения: при загрузке данные превращаются
в объекты Employee, Route и Trip, а при сохранении объекты
превращаются обратно в словари. Командировка в JSON хранит только
идентификаторы связанных объектов (employee_id, route_id).
"""

import json
from datetime import date
from typing import List

from models import Employee, Route, Trip
from models.employees import find_employee_by_id
from models.routes import find_route_by_id


def read_json(filename: str) -> list:
    """Прочитать список из JSON-файла; при ошибке вернуть пустой список."""
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, данные не загружены.")
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены.")
    return []


def write_json(filename: str, data: list) -> None:
    """Записать список в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_employees(filename: str) -> List[Employee]:
    """Загрузить сотрудников и создать объекты Employee."""
    return [Employee.from_data(item) for item in read_json(filename)]


def save_employees(filename: str, employees: List[Employee]) -> None:
    """Сохранить объекты Employee в JSON."""
    data = [
        {"id": item.id, "name": item.name, "position": item.position}
        for item in employees
    ]
    write_json(filename, data)


def load_routes(filename: str) -> List[Route]:
    """Загрузить маршруты и создать объекты Route."""
    return [Route.from_data(item) for item in read_json(filename)]


def save_routes(filename: str, routes: List[Route]) -> None:
    """Сохранить объекты Route в JSON."""
    data = [
        {
            "id": item.id,
            "origin": item.origin,
            "destination": item.destination,
            "transport": item.transport,
        }
        for item in routes
    ]
    write_json(filename, data)


def load_trips(
    filename: str, employees: List[Employee], routes: List[Route]
) -> List[Trip]:
    """Загрузить командировки, восстановив связи с Employee и Route.

    Если сотрудник или маршрут с указанным id не найден, запись
    пропускается: такая командировка не может быть корректным объектом.
    """
    trips = []
    for item in read_json(filename):
        employee = find_employee_by_id(employees, item["employee_id"])
        route = find_route_by_id(routes, item["route_id"])
        if employee is None or route is None:
            print(f"Командировка {item['id']} пропущена: нет связанных данных")
            continue
        trip = Trip(
            trip_id=item["id"],
            employee=employee,
            route=route,
            start_date=date.fromisoformat(item["start_date"]),
            end_date=date.fromisoformat(item["end_date"]),
            budget_limit=item["budget_limit"],
        )
        trip.expenses = item["expenses"]
        trip.is_cancelled = item["is_cancelled"]
        trips.append(trip)
    return trips


def save_trips(filename: str, trips: List[Trip]) -> None:
    """Сохранить объекты Trip в JSON, заменив ссылки на id."""
    data = [
        {
            "id": trip.id,
            "employee_id": trip.employee.id,
            "route_id": trip.route.id,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget_limit": trip.budget_limit,
            "expenses": trip.expenses,
            "is_cancelled": trip.is_cancelled,
        }
        for trip in trips
    ]
    write_json(filename, data)
