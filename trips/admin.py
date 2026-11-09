"""Регистрация моделей маршрута и командировки в админке."""
from django.contrib import admin

from .models import Route, Trip


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Отображение маршрутов в админке."""

    list_display = ("origin", "destination", "transport")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """Отображение командировок в админке."""

    list_display = (
        "pk",
        "employee",
        "route",
        "start_date",
        "end_date",
        "is_cancelled",
    )
    list_filter = ("is_cancelled",)
