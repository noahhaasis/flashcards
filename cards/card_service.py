from django.db.models import Q, Count, Prefetch
from datetime import timedelta
from django.utils import timezone
from .models import Card, Review

import random

def get_next_card_to_review(user):
    """
    Retrieves the next card for a user to review based on spaced repetition logic.

    Only cards that the user has picked to learn (created an initial Review) are considered.

    Args:
        user: The User object.

    Returns:
        The next Card object to review, or None if no cards are available or all
        reviewable cards are learned (all reviews are "Easy").
    """

    # 1. Get all cards the user has started learning (reviews exist)
    all_cards = Card.objects.filter(review__user=user).prefetch_related(
        Prefetch('review_set', queryset=Review.objects.filter(user=user).order_by('-occured_at'))
    ).distinct()

    if not all_cards.exists():
        return None  # No cards picked to learn yet

    # 2. Filter out already learned cards (all reviews are "Easy")
    learnable_cards = []
    for card in all_cards:
        reviews = card.review_set.all()
        all_easy = all(review.difficulty == 2 for review in reviews)
        if not all_easy: # If not all reviews are easy, it's learnable
            learnable_cards.append(card)

    if not learnable_cards:
        return None  # All reviewable cards are learned

    # 3. Prioritize cards based on difficulty and time since last review (simplified)
    def card_priority(card):
        reviews = card.review_set.all()
        if not reviews.exists(): # Should not happen based on step 1 logic, but for robustness
            return 0
        last_review = reviews[0]
        time_since_last_review = (timezone.now() - last_review.occured_at).total_seconds()

        if last_review.difficulty == 5: # Again - highest priority
            return 0
        elif last_review.difficulty == 1: # None - initial pick, high priority
            return 1 # Slightly lower than "Again" but still high
        elif last_review.difficulty == 4: # Hard
            return time_since_last_review / 3600
        elif last_review.difficulty == 3: # Good
            return time_since_last_review / 7200
        else:  # Easy (difficulty == 2) - lowest priority, review much later
            return float('inf') # Show last

    learnable_cards.sort(key=card_priority)

    return learnable_cards[0] if learnable_cards else None

def random_fresh_card(user = None):
    """Returns a random Card object. If a user is specified, only returns a card that is not in his review stack. Raises an exception if no cards exist."""
    count = Card.objects.count()
    if count == 0:
        raise Card.DoesNotExist("No cards found in the database.")

    if user is None:
        random_index = random.randint(0, count - 1)
        random_card = Card.objects.all()[random_index]
        return random_card

    unreviewed_cards = Card.objects.exclude(review__user=user)
    random_index = random.randint(0, unreviewed_cards.count() - 1)
    return unreviewed_cards.all()[random_index]
