from django.db import models


GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female')
)


class Actor(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)
    birthdate = models.DateField()
    gender = models.CharField(max_length=6,choices=GENDER_CHOICES)



