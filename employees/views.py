"""Представления приложения employees.

Данные получаются через Django ORM. Значения из URL и форм
используются как параметры методов ORM, а не подставляются в SQL.
"""
from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from employees.models import Employee
from trips.models import Trip


def employees(request):
    """Список сотрудников, отсортированный по ФИО."""
    employees_list = Employee.objects.order_by("name")
    context = {"employees": employees_list}
    return render(request, "employees/employee_list.html", context)


def employee_detail(request, employee_id):
    """Карточка сотрудника: данные, статус на сегодня, командировки."""
    employee = get_object_or_404(Employee, pk=employee_id)

    # Командировки сотрудника с маршрутом (обратная связь trips).
    trips = employee.trips.select_related("route").order_by("start_date")

    # Находится ли сотрудник в командировке на текущую дату.
    today = timezone.localdate()
    traveling = employee.trips.filter(
        is_cancelled=False,
        start_date__lte=today,
        end_date__gte=today,
    ).exists()

    context = {
        "employee": employee,
        "trips": trips,
        "traveling": traveling,
    }
    return render(request, "employees/employee_detail.html", context)


def available_employees(request):
    """Поиск сотрудников, свободных от командировок на выбранную дату."""
    selected_date = request.GET.get("date", "").strip()
    employees_list = []
    error = None

    if selected_date:
        try:
            parsed = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Введите дату в формате ГГГГ-ММ-ДД."
        else:
            # Идентификаторы сотрудников, занятых активной
            # командировкой на выбранную дату.
            busy_ids = Trip.objects.filter(
                is_cancelled=False,
                start_date__lte=parsed,
                end_date__gte=parsed,
            ).values_list("employee_id", flat=True)
            employees_list = Employee.objects.exclude(
                pk__in=busy_ids
            ).order_by("name")

    context = {
        "employees": employees_list,
        "selected_date": selected_date,
        "error": error,
    }
    return render(request, "employees/available.html", context)
