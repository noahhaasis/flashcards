from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cards/<int:card_id>/correct", views.index, name="index"),
    path("cards/<int:card_id>/incorrect", views.index, name="index"),
]
