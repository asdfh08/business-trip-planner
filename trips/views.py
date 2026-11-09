"""Представления приложения trips.

Данные получаются через Django ORM. Значения из строки запроса
используются как параметры методов ORM; прямые SQL-запросы и
объединения таблиц (JOIN) вручную не пишутся.
"""
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render

from employees.models import Employee
from trips.models import Route, Trip

# Значение параметра status -> значение поля is_cancelled.
STATUS_FILTERS = {"active": False, "cancelled": True}

# Значение параметра sort -> поле модели для сортировки.
SORT_FIELDS = {
    "date": "start_date",
    "employee": "employee__name",
    "route": "route__destination",
}


def trips(request):
    """Список командировок: фильтры, сортировка и пагинация."""
    status = request.GET.get("status", "all")
    employee_id = request.GET.get("employee", "").strip()
    route_id = request.GET.get("route", "").strip()
    booking_date = request.GET.get("date", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    # Связанные объекты загружаются одним запросом (select_related).
    trips_data = Trip.objects.select_related("employee", "route")

    # Фильтрация по статусу (все / активные / отменённые).
    if status in STATUS_FILTERS:
        trips_data = trips_data.filter(
            is_cancelled=STATUS_FILTERS[status]
        )
    else:
        status = "all"

    # Фильтрация по дате: командировки, покрывающие выбранный день.
    if booking_date:
        try:
            parsed = datetime.strptime(booking_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Введите корректную дату."
        else:
            trips_data = trips_data.filter(
                start_date__lte=parsed,
                end_date__gte=parsed,
            )

    # Фильтрация по сотруднику и маршруту через внешние ключи.
    if employee_id.isdigit():
        trips_data = trips_data.filter(employee_id=int(employee_id))
    if route_id.isdigit():
        trips_data = trips_data.filter(route_id=int(route_id))

    # Сортировка по разрешённому полю; id — стабильный порядок.
    sort_field = SORT_FIELDS.get(sort, "start_date")
    trips_data = trips_data.order_by(sort_field, "id")

    # Постраничный вывод: по 5 записей на страницу.
    paginator = Paginator(trips_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "trips": page_obj,
        "page_obj": page_obj,
        "status": status,
        "selected_employee": employee_id,
        "selected_route": route_id,
        "booking_date": booking_date,
        "sort": sort,
        "error": error,
        "employees": Employee.objects.order_by("name"),
        "routes": Route.objects.order_by("origin", "destination"),
    }
    return render(request, "trips/trip_list.html", context)


def trip_detail(request, trip_id):
    """Карточка командировки со сведениями о сотруднике и маршруте."""
    trip = get_object_or_404(
        Trip.objects.select_related("employee", "route"),
        pk=trip_id,
    )
    return render(request, "trips/trip_detail.html", {"trip": trip})


def statistics(request):
    """Статистика командировок: сводка, группировки, превышения."""
    try:
        min_trips = int(request.GET.get("min_trips", 1))
    except ValueError:
        min_trips = 1

    # Сводка по всем командировкам (агрегатные функции).
    summary = Trip.objects.aggregate(
        total_trips=Count("id"),
        active_trips=Count("id", filter=Q(is_cancelled=False)),
        cancelled_trips=Count("id", filter=Q(is_cancelled=True)),
        total_expenses=Sum("expenses"),
        avg_budget=Avg("budget_limit"),
    )

    # Количество активных командировок и расходы по сотрудникам.
    by_employee = (
        Employee.objects
        .annotate(
            employee_name=F("name"),
            trips_count=Count(
                "trips",
                filter=Q(trips__is_cancelled=False),
            ),
            total_expenses=Coalesce(
                Sum(
                    "trips__expenses",
                    filter=Q(trips__is_cancelled=False),
                ),
                0.0,
            ),
        )
        .values("employee_name", "trips_count", "total_expenses")
        .order_by("-trips_count", "name")
    )

    # Популярность маршрутов.
    by_route = (
        Route.objects
        .annotate(
            trips_count=Count(
                "trips",
                filter=Q(trips__is_cancelled=False),
            ),
        )
        .values("origin", "destination", "transport", "trips_count")
        .order_by("-trips_count", "destination")
    )

    # Сотрудники с числом активных командировок больше порога (HAVING).
    frequent = (
        Employee.objects
        .annotate(
            employee_name=F("name"),
            trips_count=Count(
                "trips",
                filter=Q(trips__is_cancelled=False),
            ),
        )
        .filter(trips_count__gt=min_trips)
        .values("employee_name", "trips_count")
        .order_by("-trips_count")
    )

    # Командировки с превышением бюджета.
    over_budget = (
        Trip.objects
        .filter(is_cancelled=False, expenses__gt=F("budget_limit"))
        .annotate(
            employee_name=F("employee__name"),
            destination=F("route__destination"),
            overrun=F("expenses") - F("budget_limit"),
        )
        .values(
            "id",
            "employee_name",
            "destination",
            "budget_limit",
            "expenses",
            "overrun",
        )
        .order_by("-overrun")
    )

    context = {
        "summary": summary,
        "by_employee": by_employee,
        "by_route": by_route,
        "frequent": frequent,
        "over_budget": over_budget,
        "min_trips": min_trips,
    }
    return render(request, "trips/statistics.html", context)
