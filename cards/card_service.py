from .models import Card, Review

from datetime import timedelta
from django.db.models import Subquery, OuterRef, Case, When, Value, F, ExpressionWrapper, DateTimeField, DurationField, Min
from django.utils import timezone

import random

def get_next_card_to_review(user):
    """
    Determines the next card to review for the given user using a simple spaced repetition algorithm.
    
    A card is only eligible if it has at least one review entry. Each card's next review time is computed 
    based on its most recent review's timestamp and difficulty level, as follows:
      - difficulty=1 ("none"): review immediately (0 delay)
      - difficulty=2 ("easy"): delay 2 days
      - difficulty=3 ("good"): delay 1 day
      - difficulty=4 ("hard"): delay 10 minutes
      - difficulty=5 ("again"): delay 2 minutes

    The function returns a dictionary with:
      - "card": the Card instance to review now if available, otherwise None.
      - "status": one of:
            "no_cards"    -> no cards exist for review,
            "available"   -> at least one card is due for review,
            "all_reviewed"-> cards exist but none are due now.
      - "next_review_at": if no card is due, the datetime when the next card becomes available; if a card is due,
                          the due time of that card; or None if no cards exist.
    """
    now = timezone.now()
    
    # Subquery to get the most recent review for each card for the user.
    latest_review_qs = Review.objects.filter(
        card=OuterRef('pk'),
        user=user
    ).order_by('-occured_at')
    
    # Build a queryset for Cards that have at least one review for this user.
    qs = Card.objects.filter(review__user=user).distinct().annotate(
        last_review=Subquery(latest_review_qs.values('occured_at')[:1]),
        last_difficulty=Subquery(latest_review_qs.values('difficulty')[:1])
    ).annotate(
        review_delay=Case(
            When(last_difficulty=1, then=Value(timedelta(minutes=0))),
            When(last_difficulty=2, then=Value(timedelta(days=2))),
            When(last_difficulty=3, then=Value(timedelta(days=1))),
            When(last_difficulty=4, then=Value(timedelta(minutes=10))),
            When(last_difficulty=5, then=Value(timedelta(minutes=2))),
            default=Value(timedelta(days=1)),
            output_field=DurationField()
        )
    ).annotate(
        next_review=ExpressionWrapper(F('last_review') + F('review_delay'), output_field=DateTimeField())
    )
    
    # No cards exist for review.
    if not qs.exists():
         return {
             "card": None,
             "status": "no_cards",
             "next_review_at": None,
         }
    
    # Check if there are any cards due for review.
    due_qs = qs.filter(next_review__lte=now).order_by('next_review')
    if due_qs.exists():
         next_card = due_qs.first()
         return {
             "card": next_card,
             "status": "available",
             "next_review_at": next_card.next_review,
         }
    else:
         # All cards have been reviewed; get the soonest upcoming review time.
         next_review_at = qs.aggregate(Min('next_review'))['next_review__min']
         return {
             "card": None,
             "status": "all_reviewed",
             "next_review_at": next_review_at,
         }

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
