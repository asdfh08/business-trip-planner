"""Функции для работы с маршрутами — словарём routes."""


def add_route(
    routes: dict[int, dict], origin: str, destination: str, transport: str
) -> int:
    """Добавить маршрут в словарь routes.

    Идентификатор формируется автоматически. Возвращает id маршрута.
    """
    new_id = max(routes.keys(), default=0) + 1
    routes[new_id] = {
        "id": new_id,
        "origin": origin,
        "destination": destination,
        "transport": transport,
    }
    return new_id


def find_route(routes: dict[int, dict], query: str) -> list[dict]:
    """Найти маршруты по подстроке города отправления или назначения."""
    query_lower = query.lower()
    return [
        route
        for route in routes.values()
        if query_lower in route["origin"].lower()
        or query_lower in route["destination"].lower()
    ]


def get_route(routes: dict[int, dict], route_id: int) -> dict | None:
    """Вернуть маршрут по идентификатору или None, если не найден."""
    return routes.get(route_id)


def get_route_description(route: dict) -> str:
    """Вернуть текстовое описание маршрута."""
    return f"{route['origin']} → {route['destination']} ({route['transport']})"
