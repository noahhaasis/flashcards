from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template import loader
from .models import Card, Guess

import random

def index(request):
    context = { "card": get_random_card() }
    return render(request, "index.html", context)

@require_POST
def guessed_correctly(request, card_id):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_id)
        Guess.objects.create(user=request.user, card=card, correct=True)

    context = { "card": get_random_card() }
    return render(request, "card.html", context)


@require_POST
def guessed_incorrectly(request, card_id):
    if request.user.is_authenticated:
        card = get_object_or_404(Card, pk=card_id)
        Guess.objects.create(user=request.user, card=card, correct=False)

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
