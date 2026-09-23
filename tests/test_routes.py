"""Автоматизированные тесты функций работы с маршрутами."""

from routes import add_route, find_route, get_route


def test_add_route():
    routes = {}
    new_id = add_route(routes, "Москва", "Казань", "Поезд")
    assert len(routes) == 1
    assert new_id == 1


def test_find_route():
    routes = {}
    add_route(routes, "Москва", "Казань", "Поезд")
    result = find_route(routes, "казань")
    assert len(result) == 1
    assert result[0]["destination"] == "Казань"


def test_get_route():
    routes = {}
    new_id = add_route(routes, "Москва", "Казань", "Поезд")
    route = get_route(routes, new_id)
    assert route is not None
    assert route["transport"] == "Поезд"
