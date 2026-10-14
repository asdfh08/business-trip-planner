"""Представления приложения trips."""
from django.shortcuts import render

from models.trips import find_trip_by_id
from storage import load_employees, load_routes, load_trips


def get_trips_list():
    """Загрузить все командировки."""
    employees_list = load_employees("data/employees.json")
    routes_list = load_routes("data/routes.json")
    return load_trips("data/trips.json", employees_list, routes_list)


def trips(request):
    """Список командировок."""
    context = {"trips": get_trips_list()}
    return render(request, "trips/trip_list.html", context)


def trip_detail(request, trip_id):
    """Карточка командировки."""
    trip = find_trip_by_id(get_trips_list(), trip_id)
    context = {"trip": trip}
    return render(
        request, "trips/trip_detail.html", context,
        status=404 if trip is None else 200,
    )
