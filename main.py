from datetime import date
 
# Простые типы данных: сотрудник и параметры командировки
employee_name = "Иванова Мария Сергеевна"
destination = "Санкт-Петербург"
trip_start = date(2026, 10, 5)
trip_end = date(2026, 10, 10)
budget_limit = 50000
planned_expenses = "42500"  # строка, требует преобразования типа перед сравнением
 
 
def calculate_trip_duration(start_date, end_date):
    """Возвращает продолжительность командировки в днях."""
    duration = (end_date - start_date).days
    return duration
 
 
def check_budget_status(expenses_str, limit):
    """Преобразует расходы из строки в число и сравнивает с лимитом бюджета."""
    expenses = float(expenses_str)
    if expenses > limit:
        return "Бюджет превышен"
    elif expenses == limit:
        return "Бюджет использован полностью"
    else:
        return "Расходы в пределах бюджета"
 
 
def get_trip_summary(name, dest, start, end):
    """Формирует краткую сводку по командировке сотрудника."""
    duration = calculate_trip_duration(start, end)
    return f"Сотрудник {name} отправляется в командировку в город {dest} на {duration} дн."
 
 
if __name__ == "__main__":
    print(get_trip_summary(employee_name, destination, trip_start, trip_end))
    print(f"Бюджет командировки: {budget_limit} руб.")
    print(check_budget_status(planned_expenses, budget_limit))
 

