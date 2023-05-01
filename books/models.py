from django.db import models

from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    summary = models.TextField(null=True)

    users = models.ManyToManyField(User, related_name="books")
