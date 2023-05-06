from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, ListAPIView

from users.models import User
from .models import Copy, Loan
from .serializers import CopySerializer, LoanSerializer
from django.shortcuts import get_object_or_404
from books.models import Book
from .permissions import isCollaborator, isCollaboratorOrGet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta
from rest_framework.views import Response, status


class CopiesView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaboratorOrGet]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.request.data["book_id"])
        serializer.save(book=book)

class CopiesDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaboratorOrGet]
    
    queryset = Copy.objects.all()
    serializer_class = CopySerializer

class CopiesListByBookView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaboratorOrGet]

    def get_queryset(self):
        book = get_object_or_404(Book, pk=self.kwargs["pk"])
        return Copy.objects.filter(book=book)
    serializer_class = CopySerializer

class LoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaborator]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["id"])
        return Loan.objects.filter(user=user)
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.have_permission is not None and request.user.have_permission > date.today():
            return Response({"message": f"User still blocked until {request.user.have_permission}!"}, status.HTTP_403_FORBIDDEN)
        try:
            self.perform_create(serializer)
        except ReferenceError:
            return Response({"message": "Copy unavailable for loan!"}, status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = get_object_or_404(User, id=self.kwargs["id"])
        user.save()
        copy = get_object_or_404(Copy, pk=self.kwargs["pk"])
        if copy.available == False:
            raise ReferenceError("Copy unavailable for loan!")
        copy.available = False
        copy.save()

        serializer.save(user=user, copy=copy)

class LoanReturnView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def patch(self, request, *args, **kwargs):
        loan = get_object_or_404(Loan.objects.all(), id=kwargs["pk"])
        if loan.copy.available:
            return Response({"message": "Copy has already been returned!"}, status.HTTP_409_CONFLICT)
        return super().patch(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class LoanHistoricUserView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)
    serializer_class = LoanSerializer

class LoanHistoricAllUserCollaboratorView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isCollaborator]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return Loan.objects.filter(user=user)
    serializer_class = LoanSerializer
# Create your views here.
