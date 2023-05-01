from django.db import models

from users.models import User
from copies.models import Copy


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(Copy, on_delete=models.CASCADE)

    start_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
