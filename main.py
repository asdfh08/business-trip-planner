"""Точка запуска приложения «Сервис планирования командировок».

Приложение работает с объектами Employee, Route и Trip. Данные
загружаются из JSON и сохраняются обратно через модуль storage.py.
"""

from typing import List

from models import Employee, Route, Trip
from models.employees import (
    add_employee,
    find_employee,
    find_employee_by_id,
    show_employees,
)
from models.routes import add_route, find_route_by_id, show_routes
from models.trips import (
    cancel_trip,
    create_trip,
    find_trip_by_id,
    get_statistics,
    show_trips,
)
from storage import (
    load_employees,
    load_routes,
    load_trips,
    save_employees,
    save_routes,
    save_trips,
)
from utils import input_date, input_float, input_int

EMPLOYEES_FILE = "data/employees.json"
ROUTES_FILE = "data/routes.json"
TRIPS_FILE = "data/trips.json"

MENU = """
=== Сервис планирования командировок ===
1. Показать сотрудников
2. Добавить сотрудника
3. Найти сотрудника по имени
4. Показать маршруты
5. Добавить маршрут
6. Показать командировки
7. Добавить командировку
8. Отменить командировку
9. Внести расходы по командировке
10. Показать статистику по расходам
0. Выход
"""


def handle_add_employee(employees: List[Employee]) -> None:
    """Добавить сотрудника по данным, введённым пользователем."""
    name = input("Имя сотрудника: ")
    position = input("Должность: ")
    employee = add_employee(employees, name, position)
    print(f"Сотрудник добавлен: {employee}")


def handle_find_employee(employees: List[Employee]) -> None:
    """Найти сотрудников по подстроке имени."""
    query = input("Подстрока имени: ")
    show_employees(find_employee(employees, query))


def handle_add_route(routes: List[Route]) -> None:
    """Добавить маршрут по данным, введённым пользователем."""
    origin = input("Город отправления: ")
    destination = input("Город назначения: ")
    transport = input("Транспорт (поезд/самолёт/автомобиль): ")
    route = add_route(routes, origin, destination, transport)
    print(f"Маршрут добавлен: {route.id}. {route}")


def create_new_trip(
    trips: List[Trip], employees: List[Employee], routes: List[Route]
) -> None:
    """Сценарий создания командировки: сотрудник + маршрут + даты."""
    employee = find_employee_by_id(employees, input_int("Id сотрудника: "))
    if employee is None:
        print("Сотрудник с таким id не найден.")
        return
    route = find_route_by_id(routes, input_int("Id маршрута: "))
    if route is None:
        print("Маршрут с таким id не найден.")
        return
    start_date = input_date("Дата начала (ДД.ММ.ГГГГ): ")
    end_date = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
    budget_limit = input_float("Лимит бюджета, руб.: ")
    try:
        trip = create_trip(
            trips, employee, route, start_date, end_date, budget_limit
        )
    except ValueError as error:
        print(f"Не удалось создать командировку: {error}")
        return
    if trip is None:
        print("Сотрудник уже находится в другой командировке в этот период.")
        return
    print(f"Командировка создана: {trip}")


def handle_cancel_trip(trips: List[Trip]) -> None:
    """Отменить командировку по id."""
    if cancel_trip(trips, input_int("Id командировки для отмены: ")):
        print("Командировка отменена.")
    else:
        print("Командировка с таким id не найдена.")


def handle_set_expenses(trips: List[Trip]) -> None:
    """Внести расходы и показать результат сверки с бюджетом."""
    trip = find_trip_by_id(trips, input_int("Id командировки: "))
    if trip is None:
        print("Командировка с таким id не найдена.")
        return
    trip.set_expenses(input_float("Фактические расходы, руб.: "))
    print(trip.get_budget_status())


def show_statistics(trips: List[Trip]) -> None:
    """Вывести краткую статистику по командировкам."""
    stats = get_statistics(trips)
    print(f"Всего командировок: {stats['total_trips']}")
    print(f"Запланировано: {stats['active_trips']}")
    print(f"Отменено: {stats['cancelled_trips']}")
    print(f"Суммарные расходы: {stats['total_expenses']} руб.")


def main() -> None:
    """Загрузить данные, запустить меню и сохранить данные при выходе."""
    employees = load_employees(EMPLOYEES_FILE)
    routes = load_routes(ROUTES_FILE)
    trips = load_trips(TRIPS_FILE, employees, routes)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_employees(employees)
        elif choice == "2":
            handle_add_employee(employees)
        elif choice == "3":
            handle_find_employee(employees)
        elif choice == "4":
            show_routes(routes)
        elif choice == "5":
            handle_add_route(routes)
        elif choice == "6":
            show_trips(trips)
        elif choice == "7":
            create_new_trip(trips, employees, routes)
        elif choice == "8":
            handle_cancel_trip(trips)
        elif choice == "9":
            handle_set_expenses(trips)
        elif choice == "10":
            show_statistics(trips)
        elif choice == "0":
            save_employees(EMPLOYEES_FILE, employees)
            save_routes(ROUTES_FILE, routes)
            save_trips(TRIPS_FILE, trips)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
