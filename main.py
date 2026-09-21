"""Точка запуска приложения «Сервис планирования командировок»."""

from employees import add_employee, find_employee
from storage import (
    load_employees,
    load_trips,
    save_employees,
    save_trips,
)
from trips import (
    cancel_trip,
    check_budget_status,
    create_trip,
    get_statistics,
    get_trip_summary,
    sort_trips_by_date,
)
from utils import input_date, input_float, input_int

EMPLOYEES_FILE = "data/employees.json"
TRIPS_FILE = "data/trips.json"

MENU = """
=== Сервис планирования командировок ===
1. Показать сотрудников
2. Добавить сотрудника
3. Найти сотрудника по имени
4. Показать командировки
5. Добавить командировку
6. Отменить командировку
7. Внести расходы по командировке
8. Показать статистику по расходам
0. Выход
"""


def show_employees(employees: dict[int, dict]) -> None:
    """Вывести список сотрудников."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    for employee in employees.values():
        print(f"{employee['id']}. {employee['name']} — {employee['position']}")


def show_trips(employees: dict[int, dict], trips: list[dict]) -> None:
    """Вывести список командировок, отсортированных по дате начала."""
    if not trips:
        print("Список командировок пуст.")
        return
    for trip in sort_trips_by_date(trips):
        print(
            f"{trip['id']}. {get_trip_summary(employees, trip)} "
            f"[{trip['status']}]"
        )


def handle_add_employee(employees: dict[int, dict]) -> None:
    """Обработать сценарий добавления сотрудника."""
    name = input("Имя сотрудника: ")
    position = input("Должность: ")
    new_id = add_employee(employees, name, position)
    print(f"Сотрудник добавлен, id = {new_id}")


def handle_add_trip(employees: dict[int, dict], trips: list[dict]) -> None:
    """Обработать сценарий добавления командировки."""
    employee_id = input_int("Id сотрудника: ")
    if employee_id not in employees:
        print("Сотрудник с таким id не найден.")
        return
    destination = input("Город назначения: ")
    start_date = input_date("Дата начала (ДД.ММ.ГГГГ): ")
    end_date = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
    budget_limit = input_float("Лимит бюджета, руб.: ")
    try:
        trip = create_trip(
            trips, employee_id, destination, start_date, end_date, budget_limit
        )
    except ValueError as error:
        print(f"Не удалось создать командировку: {error}")
        return
    print(f"Командировка создана, id = {trip['id']}")


def handle_cancel_trip(trips: list[dict]) -> None:
    """Обработать сценарий отмены командировки."""
    trip_id = input_int("Id командировки для отмены: ")
    if cancel_trip(trips, trip_id):
        print("Командировка отменена.")
    else:
        print("Командировка с таким id не найдена.")


def handle_check_budget(trips: list[dict]) -> None:
    """Обработать сценарий проверки расходов по командировке."""
    trip_id = input_int("Id командировки: ")
    trip = next((item for item in trips if item["id"] == trip_id), None)
    if trip is None:
        print("Командировка с таким id не найдена.")
        return
    expenses = input_float("Фактические расходы, руб.: ")
    trip["expenses"] = expenses
    print(check_budget_status(expenses, trip["budget_limit"]))


def show_statistics(trips: list[dict]) -> None:
    """Вывести краткую статистику по командировкам."""
    stats = get_statistics(trips)
    print(f"Всего командировок: {stats['total_trips']}")
    print(f"Запланировано: {stats['active_trips']}")
    print(f"Отменено: {stats['cancelled_trips']}")
    print(f"Суммарные расходы: {stats['total_expenses']} руб.")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    employees = load_employees(EMPLOYEES_FILE)
    trips = load_trips(TRIPS_FILE)

    while True:
        print(MENU)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_employees(employees)
        elif choice == "2":
            handle_add_employee(employees)
        elif choice == "3":
            query = input("Подстрока имени: ")
            found = find_employee(employees, query)
            show_employees({item["id"]: item for item in found})
        elif choice == "4":
            show_trips(employees, trips)
        elif choice == "5":
            handle_add_trip(employees, trips)
        elif choice == "6":
            handle_cancel_trip(trips)
        elif choice == "7":
            handle_check_budget(trips)
        elif choice == "8":
            show_statistics(trips)
        elif choice == "0":
            save_employees(EMPLOYEES_FILE, employees)
            save_trips(TRIPS_FILE, trips)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
