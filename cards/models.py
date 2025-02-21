from django.db import models

import os

class Card(models.Model):
    german = models.CharField(max_length=200)
    turkish = models.CharField(max_length=200)
    image_name = models.CharField(max_length=200)

    @property
    def image_url(self):
        return os.path.join('images', f'{self.image_name}')

