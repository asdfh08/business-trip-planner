from django.http import HttpResponse

from homepage.views import page
from models.trips import find_trip_by_id
from storage import load_employees, load_routes, load_trips


def get_trips_list():
    employees_list = load_employees("data/employees.json")
    routes_list = load_routes("data/routes.json")
    return load_trips("data/trips.json", employees_list, routes_list)


def trips(request):
    items = ""
    for trip in get_trips_list():
        status = "отменена" if trip.is_cancelled else "запланирована"
        badge = "bg-secondary" if trip.is_cancelled else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/trips/{trip.id}/">
                {trip.employee.name}: {trip.route.destination},
                {trip.start_date:%d.%m.%Y}–{trip.end_date:%d.%m.%Y}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Командировки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Командировки", content))


def trip_detail(request, trip_id):
    trip = find_trip_by_id(get_trips_list(), trip_id)

    if trip is None:
        content = """
        <h1 class="text-danger">Командировка не найдена</h1>
        <a href="/trips/" class="btn btn-outline-secondary">
            ← к списку командировок
        </a>
        """
        return HttpResponse(
            page("Командировка не найдена", content),
            status=404,
        )

    status = "отменена" if trip.is_cancelled else "запланирована"
    badge = "bg-secondary" if trip.is_cancelled else "bg-success"
    expenses = "не внесены" if trip.expenses is None else trip.expenses

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Командировка №{trip.id}</h5>
            <p class="card-text">
                Сотрудник: {trip.employee.name} ({trip.employee.position})
            </p>
            <p class="card-text">Маршрут: {trip.route}</p>
            <p class="card-text">
                Даты: {trip.start_date:%d.%m.%Y}–{trip.end_date:%d.%m.%Y}
                ({trip.duration()} дн.)
            </p>
            <p class="card-text">
                Бюджет: {trip.budget_limit} руб.,
                расходы: {expenses}
            </p>
            <p class="card-text">
                Сверка с бюджетом: {trip.get_budget_status()}
            </p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/trips/" class="btn btn-outline-secondary">
                ← к списку командировок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Командировка №{trip.id}", content),
        status=200,
    )
