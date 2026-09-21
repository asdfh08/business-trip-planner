"""Автоматизированные тесты функций работы с сотрудниками."""

from employees import add_employee, find_employee, get_employee


def test_add_employee():
    employees = {}
    new_id = add_employee(employees, "Иванова Мария", "Менеджер")
    assert len(employees) == 1
    assert new_id == 1


def test_add_employee_generates_next_id():
    employees = {}
    add_employee(employees, "Иванова Мария", "Менеджер")
    second_id = add_employee(employees, "Петров Андрей", "Инженер")
    assert second_id == 2


def test_find_employee():
    employees = {}
    add_employee(employees, "Иванова Мария", "Менеджер")
    result = find_employee(employees, "мария")
    assert len(result) == 1
    assert result[0]["name"] == "Иванова Мария"


def test_find_employee_no_match():
    employees = {}
    add_employee(employees, "Иванова Мария", "Менеджер")
    assert find_employee(employees, "Сидоров") == []


def test_get_employee():
    employees = {}
    new_id = add_employee(employees, "Иванова Мария", "Менеджер")
    employee = get_employee(employees, new_id)
    assert employee is not None
    assert employee["position"] == "Менеджер"
