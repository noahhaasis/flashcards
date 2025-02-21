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

class Guess(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guessed_at = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField()

    def __str__(self):
        if self.correct:
            return f"Correct guess by {self.user.username} on {self.card}"
        else:
            return f"Incorrect guess by {self.user.username} on {self.card}"


