"""Тесты страниц Django, получающих данные из SQLite (ПР7)."""

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripplanner.settings")
django.setup()

from django.test import Client  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402

setup_test_environment()


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize(
    "url",
    [
        "/",
        "/employees/",
        "/employees/1/",
        "/employees/available/",
        "/employees/available/?date=2026-11-03",
        "/trips/",
        "/trips/?status=active",
        "/trips/1/",
        "/trips/statistics/",
    ],
)
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


def test_unknown_objects_return_404(client):
    assert client.get("/employees/999/").status_code == 404
    assert client.get("/trips/999/").status_code == 404


def test_employee_list_from_database(client):
    response = client.get("/employees/")
    assert "Иванова Мария Сергеевна" in response.content.decode()


def test_available_employees_excludes_busy(client):
    response = client.get("/employees/available/?date=2026-11-03")
    content = response.content.decode()
    assert "Сидорова Елена Павловна" in content
    assert "Петров Андрей Викторович" not in content


def test_trip_status_filter(client):
    response = client.get("/trips/?status=cancelled")
    assert len(response.context["trips"]) == 1


def test_trip_detail_budget_status(client):
    response = client.get("/trips/5/")
    assert "Бюджет превышен" in response.content.decode()


def test_statistics_having_threshold(client):
    response = client.get("/trips/statistics/?min_trips=99")
    assert list(response.context["frequent"]) == []
