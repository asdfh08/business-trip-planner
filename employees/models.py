"""Модель предметной области: сотрудник."""
from django.db import models


class Employee(models.Model):
    """Сотрудник, которого направляют в командировку."""

    name = models.CharField(
        max_length=200,
        verbose_name="ФИО сотрудника",
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        """Текстовое представление сотрудника."""
        return self.name
