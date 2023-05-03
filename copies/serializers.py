from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Copy
from books.models import Book
from django.forms.models import model_to_dict

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
