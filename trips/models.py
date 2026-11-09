"""Модели предметной области: маршрут и командировка."""
from django.db import models


class Route(models.Model):
    """Маршрут командировки: откуда, куда и каким транспортом."""

    origin = models.CharField(
        max_length=200,
        verbose_name="Город отправления",
    )
    destination = models.CharField(
        max_length=200,
        verbose_name="Город назначения",
    )
    transport = models.CharField(
        max_length=100,
        verbose_name="Транспорт",
    )

    class Meta:
        ordering = ["origin", "destination"]
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        """Текстовое представление маршрута."""
        return f"{self.origin} → {self.destination} ({self.transport})"


class Trip(models.Model):
    """Командировка: связывает сотрудника и маршрут."""

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        related_name="trips",
        verbose_name="Сотрудник",
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        related_name="trips",
        verbose_name="Маршрут",
    )
    start_date = models.DateField(
        verbose_name="Дата начала",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания",
    )
    budget_limit = models.FloatField(
        verbose_name="Лимит бюджета",
    )
    # Расходы могут быть ещё не внесены, поэтому допускается NULL.
    expenses = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Фактические расходы",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Командировка отменена",
    )

    class Meta:
        ordering = ["start_date", "pk"]
        verbose_name = "Командировка"
        verbose_name_plural = "Командировки"

    @property
    def duration(self):
        """Продолжительность командировки в днях."""
        return (self.end_date - self.start_date).days

    @property
    def budget_status(self):
        """Сверка фактических расходов с лимитом бюджета."""
        if self.expenses is None:
            return "Расходы ещё не внесены"
        if self.expenses > self.budget_limit:
            return "Бюджет превышен"
        if self.expenses == self.budget_limit:
            return "Бюджет использован полностью"
        return "Расходы в пределах бюджета"

    def cancel(self):
        """Отменить командировку и сохранить изменение."""
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        """Текстовое представление командировки."""
        return f"Командировка #{self.pk}: {self.employee.name}"
