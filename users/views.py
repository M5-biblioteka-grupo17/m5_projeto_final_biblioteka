from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import UserSerializer
from .permissions import IsLibraryCollaboratorOrOwner


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLibraryCollaboratorOrOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        exclude=True
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
