from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .movies import Movie

User = get_user_model()


class Comments(models.Model):
    todo_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)