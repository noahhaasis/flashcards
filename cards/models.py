from django.db import models
from django.contrib.auth.models import User

import os

class Card(models.Model):
    german = models.CharField(max_length=200)
    turkish = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)

    @property
    def image_url(self):
        return os.path.join('images', f'{self.image_name}')

    def __str__(self):
        return f"{self.german} <=> {self.turkish}"

class Review(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    occured_at = models.DateTimeField(auto_now_add=True)
    # If the difficulty is None then the user picked this card to learn but hasn't reviewed it yet.
    difficulty = models.PositiveSmallIntegerField(
        choices=(
            (1, "none"),
            (2, "easy"),
            (3, "good"),
            (4, "hard"),
            (5, "again"),
        )
    )

    def __str__(self):
        if self.correct:
            return f"Correct guess by {self.user.username} on {self.card}"
        else:
            return f"Incorrect guess by {self.user.username} on {self.card}"


