from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Copy
from .serializers import CopySerializer
from django.shortcuts import get_object_or_404
from books.models import Book
from .permissions import isCollaboratorOrGet
from rest_framework_simplejwt.authentication import JWTAuthentication

class CopiesView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaboratorOrGet]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.request.data["book_id"])
        serializer.save(book)

class CopiesDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaboratorOrGet]
    
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

# Create your views here.
