from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=500, blank=True)
    genre = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title