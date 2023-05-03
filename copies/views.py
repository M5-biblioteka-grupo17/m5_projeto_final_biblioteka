from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import Copy, Loan
from .serializers import CopySerializer
from django.shortcuts import get_object_or_404
from books.models import Book
from .permissions import isCollaboratorOrGet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime
from rest_framework.views import Response, status


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

class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)
    serializer_class = CopySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ReferenceError:
            return Response({"message": "No copies available for this book!"}, status.HTTP_400_BAD_REQUEST)
        except PermissionError:
            return Response({"message": "The user has not return the book!"}, status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        copy = get_object_or_404(Copy, pk=self.kwargs["pk"])

        copy.reserved_copy += 1

        if copy.reserved_copy == copy.amount:
            copy.available = False
        
        if copy.available == False:
            raise ReferenceError("No copies available for this book!")
        
        if Loan.objects.filter(user=self.request.user, return_date=datetime.datetime.now(), is_returned=False).count() > 0 or self.request.user.have_permission == False:
            self.request.user.have_permission = False
            self.request.user.save()
            raise PermissionError("The user has not return the book!")
        
        copy.save()

        return_date = datetime.datetime.now() + datetime.timedelta(days=1)

        if return_date.strftime("%a") == "Sat":
            return_date = return_date + datetime.timedelta(days=2)
        if return_date.strftime("%a") == "Sun":
            return_date = return_date + datetime.timedelta(days=1)
        
        serializer.save(user=self.request.user, copy=copy, return_date=return_date)

# Create your views here.
