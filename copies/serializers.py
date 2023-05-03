from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from .models import Copy
from books.models import Book
from django.forms.models import model_to_dict
from users.serializers import UserSerializer
from .models import Loan

class CopySerializer(serializers.ModelSerializer):
    book_id = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Copy.objects.all(),
                message="This book already has a copy. If you want to change the amount, delete this copy and change the new amount!"
            )
        ]
    )
    book = serializers.SerializerMethodField(read_only=True)

    def get_book(self, obj):
        book = Book.objects.get(id=obj.books_id)
        found_book = model_to_dict(book)
        return found_book
    
    class Meta:
        model = Copy
        fields = ["id", "book_id", "amount", "available", "reserved_copy"]

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = ["id", "user", "copy", "start_date", "return_date", "is_returned"]
        read_only_fields = ["id", "user", "copy", "start_date", "return_date", "is_returned"]
    
    def update(self, instance, validated_data):
        copy = Copy.objects.filter(pk=instance.copy.id)
        copy.reserved_copy -= 1
        copy.available = True
        copy.save()

        instance.is_returned = True
        instance.save()

        user = User.objects.filter(pk=validated_data["user"].id)
        user.have_permission = True
        user.save()

        return instance