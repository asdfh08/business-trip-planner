"""Тесты класса Route и функций работы с маршрутами."""

from models import Route
from models.routes import add_route, find_route, find_route_by_id


def test_route_creation():
    route = Route(1, "Москва", "Казань", "Поезд")
    assert route.id == 1
    assert route.origin == "Москва"
    assert route.destination == "Казань"
    assert route.transport == "Поезд"


def test_route_str():
    route = Route(1, "Москва", "Казань", "Поезд")
    assert str(route) == "Москва → Казань (Поезд)"


def test_route_from_data():
    data = {
        "id": 3,
        "origin": "Москва",
        "destination": "Сочи",
        "transport": "Самолёт",
    }
    route = Route.from_data(data)
    assert route.id == 3
    assert route.destination == "Сочи"


def test_add_route():
    routes = []
    route = add_route(routes, "Москва", "Казань", "Поезд")
    assert len(routes) == 1
    assert route.id == 1


def test_find_route():
    routes = []
    add_route(routes, "Москва", "Казань", "Поезд")
    result = find_route(routes, "казань")
    assert len(result) == 1
    assert result[0].destination == "Казань"


def test_find_route_by_id():
    routes = []
    route = add_route(routes, "Москва", "Казань", "Поезд")
    assert find_route_by_id(routes, route.id) is route
    assert find_route_by_id(routes, 99) is None
