"""Тесты класса Employee и функций работы с сотрудниками."""

from models import Employee
from models.employees import add_employee, find_employee, find_employee_by_id


def test_employee_creation():
    employee = Employee(1, "Иванова Мария", "Менеджер")
    assert employee.id == 1
    assert employee.name == "Иванова Мария"
    assert employee.position == "Менеджер"


def test_employee_str():
    employee = Employee(1, "Иванова Мария", "Менеджер")
    assert str(employee) == "1. Иванова Мария — Менеджер"


def test_employee_from_data():
    data = {"id": 2, "name": "Петров Андрей", "position": "Инженер"}
    employee = Employee.from_data(data)
    assert employee.id == 2
    assert employee.name == "Петров Андрей"


def test_add_employee():
    employees = []
    employee = add_employee(employees, "Иванова Мария", "Менеджер")
    assert len(employees) == 1
    assert employee.id == 1
    assert employees[0] is employee


def test_add_employee_generates_next_id():
    employees = []
    add_employee(employees, "Иванова Мария", "Менеджер")
    second = add_employee(employees, "Петров Андрей", "Инженер")
    assert second.id == 2


def test_find_employee():
    employees = []
    add_employee(employees, "Иванова Мария", "Менеджер")
    result = find_employee(employees, "мария")
    assert len(result) == 1
    assert result[0].name == "Иванова Мария"


def test_find_employee_no_match():
    employees = []
    add_employee(employees, "Иванова Мария", "Менеджер")
    assert find_employee(employees, "Сидоров") == []


def test_find_employee_by_id():
    employees = []
    employee = add_employee(employees, "Иванова Мария", "Менеджер")
    assert find_employee_by_id(employees, employee.id) is employee
    assert find_employee_by_id(employees, 99) is None
