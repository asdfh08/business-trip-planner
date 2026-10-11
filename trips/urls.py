from django.urls import path

from . import views

urlpatterns = [
    path("", views.trips, name="trips"),
    path("<int:trip_id>/", views.trip_detail, name="trip_detail"),
]
