from django.urls import path

from . import views

urlpatterns = [
    path("", views.employees, name="employees"),
    path(
        "<int:employee_id>/",
        views.employee_detail,
        name="employee_detail",
    ),
]
