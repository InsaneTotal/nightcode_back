from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions, status
from .models import User, TypeDocument, Roles, Status
from .serializers import UserSerializer, TypeDocumentSerializer, RolesSerializer, StatusSerializer, CurrentUserSerializer, ChangePasswordSerializer
from .permissions import IsAdminOnly
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOnly]
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], url_path='deactivate', permission_classes=[IsAdminOnly])
    def deactivate_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'Usuario desactivado'})

    @action(detail=True, methods=['post'], url_path='activate', permission_classes=[IsAdminOnly])
    def activate_user(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'Usuario activado'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOnly], url_path='change-password')
    def change_password(self, request, pk=None):
        try:
            user = self.get_object()
            serializer = ChangePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"message": "Contraseña cambiada exitosamente.",
                             "status": status.HTTP_200_OK})
        except ValidationError as e:
            return Response({"message": e.detail, "status": status.HTTP_400_BAD_REQUEST})


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data)
