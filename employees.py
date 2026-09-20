"""Функции для работы с сотрудниками — словарём employees."""


def add_employee(employees: dict[int, dict], name: str, position: str) -> int:
    """Добавить сотрудника в словарь employees.

    Идентификатор формируется автоматически как следующее свободное
    целое число. Возвращает идентификатор добавленного сотрудника.
    """
    new_id = max(employees.keys(), default=0) + 1
    employees[new_id] = {"id": new_id, "name": name, "position": position}
    return new_id


def find_employee(employees: dict[int, dict], query: str) -> list[dict]:
    """Найти сотрудников по подстроке имени (без учёта регистра)."""
    query_lower = query.lower()
    result = []
    for employee in employees.values():
        if query_lower in employee["name"].lower():
            result.append(employee)
    return result


def get_employee(employees: dict[int, dict], employee_id: int) -> dict | None:
    """Вернуть сотрудника по идентификатору или None, если не найден."""
    return employees.get(employee_id)