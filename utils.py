# обработка исключений
"""Вспомогательные функции для безопасного ввода данных пользователем."""

from datetime import date, datetime



# id сотрудника
def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется, пока пользователь
    не введёт корректное целое число.
    """
    while True:
        raw_value = input(prompt)
        try:
            return int(raw_value)
        except ValueError:
            print("Ошибка: введите целое число.")



# сумма
def input_float(prompt: str) -> float:
    """Запросить у пользователя вещественное число (например, сумму).

    При некорректном вводе запрос повторяется.
    """
    while True:
        raw_value = input(prompt)
        try:
            return float(raw_value)
        except ValueError:
            print("Ошибка: введите число (например, 42500 или 42500.50).")



# дата
def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ.

    При некорректном формате запрос повторяется.
    """
    while True:
        raw_value = input(prompt)
        try:
            return datetime.strptime(raw_value, "%d.%m.%Y").date()
        except ValueError:
            print(
                "Ошибка: введите дату в формате ДД.ММ.ГГГГ "
                "(например, 05.10.2026)."
            )
