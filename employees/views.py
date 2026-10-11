from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.employees import find_employee_by_id
from models.trips import is_employee_traveling
from storage import load_employees, load_routes, load_trips


def employees(request):
    items = ""
    for employee in load_employees("data/employees.json"):
        items += f"""
        <li class="list-group-item">
            <a href="/employees/{employee.id}/">{employee.name}</a>
            – {employee.position}
        </li>
        """
    content = f"""
    <h1>Сотрудники</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Сотрудники", content))


def employee_detail(request, employee_id):
    employees_list = load_employees("data/employees.json")
    employee = find_employee_by_id(employees_list, employee_id)

    if employee is None:
        content = """
        <h1 class="text-danger">Сотрудник не найден</h1>
        <a href="/employees/" class="btn btn-outline-secondary">
            ← к списку сотрудников
        </a>
        """
        return HttpResponse(
            page("Сотрудник не найден", content),
            status=404,
        )

    routes_list = load_routes("data/routes.json")
    trips_list = load_trips(
        "data/trips.json",
        employees_list,
        routes_list,
    )
    today = date.today()
    traveling = is_employee_traveling(trips_list, employee, today, today)
    status = "в командировке" if traveling else "на месте"
    badge = "bg-warning text-dark" if traveling else "bg-success"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{employee.name}</h5>
            <p class="card-text"><strong>ID:</strong> {employee.id}</p>
            <p class="card-text">
                <strong>Должность:</strong> {employee.position}
            </p>
            <p class="card-text">
                Статус на текущую дату:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/employees/" class="btn btn-outline-secondary">
                ← к списку сотрудников
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(employee.name, content), status=200)
