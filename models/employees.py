"""Класс Employee и функции работы с коллекцией сотрудников."""

from typing import List, Optional


class Employee:
    """Сотрудник компании, которого направляют в командировку."""

    def __init__(self, employee_id: int, name: str, position: str) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.name = name
        self.position = position

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать сотрудника из словаря, прочитанного из JSON."""
        return cls(
            employee_id=data["id"],
            name=data["name"],
            position=data["position"],
        )

    def __str__(self) -> str:
        """Вернуть строковое представление сотрудника."""
        return f"{self.id}. {self.name} — {self.position}"


def add_employee(
    employees: List[Employee], name: str, position: str
) -> Employee:
    """Создать объект Employee и добавить его в коллекцию."""
    new_id = max((employee.id for employee in employees), default=0) + 1
    employee = Employee(new_id, name, position)
    employees.append(employee)
    return employee


def find_employee(employees: List[Employee], query: str) -> List[Employee]:
    """Найти сотрудников по подстроке имени (без учёта регистра)."""
    query_lower = query.lower()
    return [
        employee
        for employee in employees
        if query_lower in employee.name.lower()
    ]


def find_employee_by_id(
    employees: List[Employee], employee_id: int
) -> Optional[Employee]:
    """Вернуть сотрудника по идентификатору или None, если не найден."""
    for employee in employees:
        if employee.id == employee_id:
            return employee
    return None


def show_employees(employees: List[Employee]) -> None:
    """Вывести список сотрудников."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    for employee in employees:
        print(employee)
