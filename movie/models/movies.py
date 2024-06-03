from django.db import models


from .actor import Actor


class Movie(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    imdb_rating = models.FloatField(null=False, blank=False)
    genre = models.CharField(max_length=150, null=False, blank=False)
    related = models.ManyToManyField(Actor, related_name='netflix_actors', blank=True)



