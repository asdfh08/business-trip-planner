# сохранение и загрузка данных проекта в JSON-файлах
"""Функции сохранения и загрузки данных проекта в JSON-файлы."""
import json
from datetime import date


def load_employees(filename: str) -> dict[int, dict]:
    """Загрузить сотрудников из JSON-файла.

    Если файл не найден или повреждён — возвращается пустой словарь,
    программа продолжает работу с чистого листа.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            raw_employees = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, сотрудники не загружены.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, сотрудники не загружены.")
        return {}
    return {int(item["id"]): item for item in raw_employees}


def save_employees(filename: str, employees: dict[int, dict]) -> None:
    """Сохранить сотрудников в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(employees.values()), file, ensure_ascii=False, indent=2)


def load_trips(filename: str) -> list[dict]:
    """Загрузить командировки из JSON-файла, преобразуя даты из строк."""
    try:
        with open(filename, encoding="utf-8") as file:
            raw_trips = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, командировки не загружены.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, командировки не загружены.")
        return []
    trips = []
    for item in raw_trips:
        item = dict(item)
        item["start_date"] = date.fromisoformat(item["start_date"])
        item["end_date"] = date.fromisoformat(item["end_date"])
        trips.append(item)
    return trips


def save_trips(filename: str, trips: list[dict]) -> None:
    """Сохранить командировки в JSON-файл, преобразуя даты в строки."""
    serializable_trips = []
    for trip in trips:
        trip_copy = dict(trip)
        trip_copy["start_date"] = trip["start_date"].isoformat()
        trip_copy["end_date"] = trip["end_date"].isoformat()
        serializable_trips.append(trip_copy)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(serializable_trips, file, ensure_ascii=False, indent=2)


def load_routes(filename: str) -> dict[int, dict]:
    """Загрузить маршруты из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            raw_routes = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, маршруты не загружены.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, маршруты не загружены.")
        return {}
    return {int(item["id"]): item for item in raw_routes}


def save_routes(filename: str, routes: dict[int, dict]) -> None:
    """Сохранить маршруты в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(routes.values()), file, ensure_ascii=False, indent=2)
def load_routes(filename: str) -> dict[int, dict]:
    """Загрузить маршруты из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            raw_routes = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, маршруты не загружены.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, маршруты не загружены.")
        return {}
    return {int(item["id"]): item for item in raw_routes}


def save_routes(filename: str, routes: dict[int, dict]) -> None:
    """Сохранить маршруты в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(list(routes.values()), file, ensure_ascii=False, indent=2)
