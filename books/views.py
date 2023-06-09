from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

from copies.models import Copy


class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        exclude=True
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class BookFollowView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get("pk")
        user = request.user

        book = get_object_or_404(Book, pk=book_id)
        book.following.add(user)

        copy = Copy.objects.filter(book=book)

        if copy and copy[0].available:
            message = "Este livro está disponível para empréstimo"
        else:
            message = "Este livro não está disponível para empréstimo"

        send_mail(
            subject='Disponibilidade do livro na biblioteka',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response(status=status.HTTP_201_CREATED)


class BookUnfollowView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        book_id = self.kwargs.get("pk")
        user = request.user

        book = get_object_or_404(Book, pk=book_id)
        book.following.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)
