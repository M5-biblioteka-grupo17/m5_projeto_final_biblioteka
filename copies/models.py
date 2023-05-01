from django.db import models

from books.models import Book
from users.models import User


class Copy(models.Model):
    amount = models.IntegerField()
    available = models.BooleanField(default=False)

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="copies"
    )
    users = models.ManyToManyField(
        User, through="loans.Loan", related_name="copies"
    )
