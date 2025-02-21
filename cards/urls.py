from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cards/<int:card_id>/correct", views.guessed_correctly, name="correct"),
    path("cards/<int:card_id>/incorrect", views.guessed_incorrectly, name="incorrect"),
]
