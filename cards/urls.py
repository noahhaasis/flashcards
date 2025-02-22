from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='cards/new', permanent=False), name="index"),
    path("cards/<int:card_id>/correct", views.guessed_correctly, name="correct"),
    path("cards/<int:card_id>/incorrect", views.guessed_incorrectly, name="incorrect"),
    path("cards/<int:card_id>/guess/form", views.get_guess_form, name="guess_form"),
    path("cards/new", views.new_cards, name="new_cards"),
    path("cards/review", views.review_cards, name="review_cards"),
    path("cards/<int:card_id>/learn", views.start_learning_card, name="learn_card")
]
