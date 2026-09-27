"""Пакет классов предметной области: сотрудник, маршрут, командировка."""

from .employees import Employee
from .routes import Route
from .trips import Trip

__all__ = ["Employee", "Route", "Trip"]

