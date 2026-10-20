from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='movie/images', default='movie/images/default.jpg')
    genre = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
