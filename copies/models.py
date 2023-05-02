from django.db import models


class Loan(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="loans")
    copy = models.ForeignKey("copies.Copy", on_delete=models.CASCADE, related_name="loans")
    start_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True)
    is_returned = models.BooleanField(default=False)


class Copy(models.Model):
    amount = models.IntegerField()
    available = models.BooleanField(default=True)
    reserved_copy = models.IntegerField(default=0)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copy"
    )
    loan = models.ManyToManyField("users.User", through="copies.Loan", related_name="loan")
