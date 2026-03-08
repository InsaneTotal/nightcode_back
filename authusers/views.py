from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from .models import User, TypeDocument, Roles, Status
from .serializers import UserSerializer, TypeDocumentSerializer, RolesSerializer, StatusSerializer
from .permissions import IsAdminOnly, IsWaitressOnly, IsBartenderOnly
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'Usuario desactivado'})


class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    permission_classes = [IsAdminOnly]
    serializer_class = TypeDocumentSerializer


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [IsAdminOnly]
    serializer_class = RolesSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    permission_classes = [IsAdminOnly]
    serializer_class = StatusSerializer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({
                'id_role': str(user.id_role.id),
                'access': access,
                'refresh': str(refresh)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
