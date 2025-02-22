from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template import loader
from .models import Card, Review
from django.contrib.auth.decorators import login_required
from .card_service import get_next_card_to_review, random_fresh_card

# New page/Backlog
def new_cards(request):
    if request.user.is_authenticated:
        context = { "card": random_fresh_card(request.user) }
        return render(request, "new.html", context)
    else:
        context = { "card": random_fresh_card() }
        return render(request, "new.html", context)

@login_required
@require_POST
def start_learning_card(request, card_id):
    card = Card.objects.get(pk=card_id)
    if card:
        Review.objects.create(user=request.user, card=card, difficulty=1)
    context = { "card": random_fresh_card(request.user) }
    return render(request, "card.html", context)



# Review page for reviewing cards

@login_required
def review_cards(request):
    context = { "card": get_next_card_to_review(request.user) }
    return render(request, "review.html", context)

def get_guess_form(request, card_id):
    return render(request, "guess_form.html", { "card_id": card_id })

@login_required
@require_POST
def guessed_correctly(request, card_id):
    difficulty = request.GET.get("difficulty")
    return reviewed_card(request, card_id, difficulty)

@login_required
@require_POST
def guessed_incorrectly(request, card_id):
    return reviewed_card(request, card_id, "again")


# Helpers
def reviewed_card(request, card_id, difficulty):
    if difficulty == "none":
        difficulty_number = 1
    elif difficulty == "easy":
        difficulty_number = 2
    elif difficulty == "good":
        difficulty_number = 3
    elif difficulty == "hard":
        difficulty_number = 4
    elif difficulty == "again":
        difficulty_number = 5


    card = Card.objects.get(pk=card_id)
    if card:
        Review.objects.create(user=request.user, card=card, difficulty=difficulty_number)

    next_card = get_next_card_to_review(request.user)
    if next_card:
        context = { "card": next_card }
        return render(request, "card.html", context)
    else:
        pass # TODO(Noah)

