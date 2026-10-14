"""Представления приложения employees."""
from datetime import date

from django.shortcuts import render

from models.employees import find_employee_by_id
from models.trips import is_employee_traveling
from storage import load_employees, load_routes, load_trips


def employees(request):
    """Список сотрудников."""
    context = {"employees": load_employees("data/employees.json")}
    return render(request, "employees/employee_list.html", context)


def employee_detail(request, employee_id):
    """Карточка сотрудника."""
    employees_list = load_employees("data/employees.json")
    employee = find_employee_by_id(employees_list, employee_id)
    traveling = False
    if employee is not None:
        routes_list = load_routes("data/routes.json")
        trips_list = load_trips(
            "data/trips.json", employees_list, routes_list
        )
        today = date.today()
        traveling = is_employee_traveling(
            trips_list, employee, today, today
        )
    context = {"employee": employee, "traveling": traveling}
    return render(
        request, "employees/employee_detail.html", context,
        status=404 if employee is None else 200,
    )
