from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template import loader
from .models import Card

import random

def index(request):
    context = { "card": get_random_card() }
    return render(request, "index.html", context)

@require_POST
def mark_correct(request, card_id):
    context = { "card": get_random_card() }
    return render(request, "card.html", context)


@require_POST
def mark_incorrect(request, card_id):
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
