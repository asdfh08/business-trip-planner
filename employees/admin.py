"""Регистрация модели сотрудника в административной панели."""
from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Отображение сотрудников в админке."""

    list_display = ("name", "position")
    search_fields = ("name", "position")
