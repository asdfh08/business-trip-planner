"""Класс Route и функции работы с коллекцией маршрутов."""

from typing import List, Optional


class Route:
    """Маршрут командировки: откуда, куда и каким транспортом."""

    def __init__(
        self, route_id: int, origin: str, destination: str, transport: str
    ) -> None:
        """Создать объект маршрута."""
        self.id = route_id
        self.origin = origin
        self.destination = destination
        self.transport = transport

    @classmethod
    def from_data(cls, data: dict) -> "Route":
        """Создать маршрут из словаря, прочитанного из JSON."""
        return cls(
            route_id=data["id"],
            origin=data["origin"],
            destination=data["destination"],
            transport=data["transport"],
        )

    def __str__(self) -> str:
        """Вернуть строковое представление маршрута."""
        return f"{self.origin} → {self.destination} ({self.transport})"


def add_route(
    routes: List[Route], origin: str, destination: str, transport: str
) -> Route:
    """Создать объект Route и добавить его в коллекцию."""
    new_id = max((route.id for route in routes), default=0) + 1
    route = Route(new_id, origin, destination, transport)
    routes.append(route)
    return route


def find_route(routes: List[Route], query: str) -> List[Route]:
    """Найти маршруты по подстроке города отправления или назначения."""
    query_lower = query.lower()
    return [
        route
        for route in routes
        if query_lower in route.origin.lower()
        or query_lower in route.destination.lower()
    ]


def find_route_by_id(routes: List[Route], route_id: int) -> Optional[Route]:
    """Вернуть маршрут по идентификатору или None, если не найден."""
    for route in routes:
        if route.id == route_id:
            return route
    return None


def show_routes(routes: List[Route]) -> None:
    """Вывести список маршрутов."""
    if not routes:
        print("Список маршрутов пуст.")
        return
    for route in routes:
        print(f"{route.id}. {route}")
