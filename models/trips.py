"""Класс Trip и функции работы с коллекцией командировок.

Командировка связывает объект сотрудника (Employee) и объект
маршрута (Route). Функции ПР1 calculate_trip_duration() и
check_budget_status() сохранены: первая стала методом duration(),
вторая осталась обычной функцией и вызывается методом
get_budget_status().
"""

from datetime import date
from typing import Iterator, List, Optional

from .employees import Employee
from .routes import Route


def check_budget_status(expenses: float, limit: float) -> str:
    """Сравнить расходы с лимитом бюджета (функция из ПР1)."""
    if expenses > limit:
        return "Бюджет превышен"
    elif expenses == limit:
        return "Бюджет использован полностью"
    else:
        return "Расходы в пределах бюджета"


class Trip:
    """Командировка сотрудника по выбранному маршруту."""

    def __init__(
        self,
        trip_id: int,
        employee: Employee,
        route: Route,
        start_date: date,
        end_date: date,
        budget_limit: float,
    ) -> None:
        """Создать объект командировки."""
        if not Trip.validate_dates(start_date, end_date):
            raise ValueError("Дата окончания раньше даты начала")
        self.id = trip_id
        self.employee = employee
        self.route = route
        self.start_date = start_date
        self.end_date = end_date
        self.budget_limit = budget_limit
        self.expenses: Optional[float] = None
        self.is_cancelled = False

    @staticmethod
    def validate_dates(start_date: date, end_date: date) -> bool:
        """Проверить, что дата окончания не раньше даты начала."""
        return end_date >= start_date

    def duration(self) -> int:
        """Вернуть продолжительность командировки в днях (из ПР1)."""
        return (self.end_date - self.start_date).days

    def cancel(self) -> None:
        """Отменить командировку."""
        self.is_cancelled = True

    def set_expenses(self, amount: float) -> None:
        """Внести фактические расходы по командировке."""
        self.expenses = amount

    def get_budget_status(self) -> str:
        """Вернуть результат сравнения расходов с бюджетом."""
        if self.expenses is None:
            return "Расходы ещё не внесены"
        return check_budget_status(self.expenses, self.budget_limit)

    def overlaps(self, start_date: date, end_date: date) -> bool:
        """Проверить, пересекается ли командировка с указанным периодом."""
        return self.start_date <= end_date and start_date <= self.end_date

    def __str__(self) -> str:
        """Вернуть строковое представление командировки."""
        status = "отменена" if self.is_cancelled else "запланирована"
        return (
            f"{self.id}. {self.employee.name}: {self.route}, "
            f"{self.start_date:%d.%m.%Y}–{self.end_date:%d.%m.%Y} "
            f"({self.duration()} дн.) [{status}]"
        )


def is_employee_traveling(
    trips: List[Trip], employee: Employee, start_date: date, end_date: date
) -> bool:
    """Проверить, занят ли сотрудник активной командировкой в период."""
    for trip in trips:
        if trip.is_cancelled or trip.employee.id != employee.id:
            continue
        if trip.overlaps(start_date, end_date):
            return True
    return False


def create_trip(
    trips: List[Trip],
    employee: Employee,
    route: Route,
    start_date: date,
    end_date: date,
    budget_limit: float,
) -> Optional[Trip]:
    """Создать командировку и добавить её в коллекцию.

    Возвращает None, если сотрудник уже в командировке в этот период.
    Если даты некорректны, конструктор Trip вызывает ValueError.
    """
    if is_employee_traveling(trips, employee, start_date, end_date):
        return None
    new_id = max((trip.id for trip in trips), default=0) + 1
    trip = Trip(new_id, employee, route, start_date, end_date, budget_limit)
    trips.append(trip)
    return trip


def find_trip_by_id(trips: List[Trip], trip_id: int) -> Optional[Trip]:
    """Вернуть командировку по идентификатору или None."""
    for trip in trips:
        if trip.id == trip_id:
            return trip
    return None


def cancel_trip(trips: List[Trip], trip_id: int) -> bool:
    """Найти командировку и вызвать её метод cancel()."""
    trip = find_trip_by_id(trips, trip_id)
    if trip is None:
        return False
    trip.cancel()
    return True


def filter_active_trips(trips: List[Trip]) -> List[Trip]:
    """Отобрать неотменённые командировки."""
    return [trip for trip in trips if not trip.is_cancelled]


def sort_trips_by_date(trips: List[Trip]) -> List[Trip]:
    """Вернуть командировки, отсортированные по дате начала."""
    return sorted(trips, key=lambda trip: trip.start_date)


def filter_expensive_trips(
    trips: List[Trip], threshold: float
) -> Iterator[Trip]:
    """Вернуть генератор командировок с расходами выше порога."""
    return (
        trip for trip in trips
        if trip.expenses is not None and trip.expenses > threshold
    )


def get_total_expenses(trips: List[Trip]) -> float:
    """Вернуть суммарные расходы по всем командировкам."""
    total = 0.0
    for trip in trips:
        if trip.expenses is not None:
            total += trip.expenses
    return total


def get_statistics(trips: List[Trip]) -> dict:
    """Собрать краткую статистику по командировкам."""
    active_trips = filter_active_trips(trips)
    return {
        "total_trips": len(trips),
        "active_trips": len(active_trips),
        "cancelled_trips": len(trips) - len(active_trips),
        "total_expenses": get_total_expenses(trips),
    }


def show_trips(trips: List[Trip]) -> None:
    """Вывести командировки, отсортированные по дате начала."""
    if not trips:
        print("Список командировок пуст.")
        return
    for trip in sort_trips_by_date(trips):
        print(trip)
