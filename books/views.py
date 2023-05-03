from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer


class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


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
