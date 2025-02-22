from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template import loader
from .models import Card, Guess

import random

def index(request):
    context = { "card": get_random_card() }
    return render(request, "index.html", context)

def new_cards(request):
    context = { "card": get_random_card() }
    return render(request, "new.html", context)

def review_cards(request):
    context = { "card": get_random_card() }
    return render(request, "review.html", context)

def get_guess_form(request, card_id):
    return render(request, "guess_form.html", { "card_id": card_id })

@require_POST
def guessed_correctly(request, card_id):
    difficulty = request.GET.get("difficulty")
    # TODO(Noah)
    return guessed(request, card_id, correct=True)

@require_POST
def guessed_incorrectly(request, card_id):
    return guessed(request, card_id, correct=False)

def guessed(request, card_id, correct):
    if request.user.is_authenticated:
        card = Card.objects.get(pk=card_id)
        if card:
            Guess.objects.create(user=request.user, card=card, correct=correct)

    context = { "card": get_random_card() }
    return render(request, "card.html", context)

def get_random_card():
    """Returns a random Card object. Raises an exception if no cards exist."""
    count = Card.objects.count()
    if count == 0:
        raise Card.DoesNotExist("No cards found in the database.")

    random_index = random.randint(0, count - 1)
    random_card = Card.objects.all()[random_index]
    return random_card
