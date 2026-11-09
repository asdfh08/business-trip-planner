"""Представления приложения homepage."""
from django.shortcuts import render

from employees.models import Employee
from trips.models import Trip


def index(request):
    """Главная страница со сводкой, полученной через Django ORM."""
    summary = {
        "employees_count": Employee.objects.count(),
        "active_trips_count": Trip.objects.filter(
            is_cancelled=False
        ).count(),
    }
    return render(request, "homepage/index.html", {"summary": summary})


def page_not_found(request, exception):
    """Собственная страница 404."""
    return render(request, "404.html", status=404)
