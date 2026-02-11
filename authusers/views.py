from rest_framework import viewsets, permissions
from .models import User, TypeDocument, Roles, Status
from .serializers import UserSerializer, TypeDocumentSerializer, RolesSerializer, StatusSerializer
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TypeDocumentSerializer


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolesSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StatusSerializer
