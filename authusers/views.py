from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from .models import User, TypeDocument, Roles, Status
from .serializers import UserSerializer, TypeDocumentSerializer, RolesSerializer, StatusSerializer
from .permissions import IsAdminOnly, IsWaitressOnly, IsBartenderOnly
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class TypeDocumentViewSet(viewsets.ModelViewSet):
    queryset = TypeDocument.objects.all()
    # permission_classes = [IsAdminOnly]
    serializer_class = TypeDocumentSerializer


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    # permission_classes = [IsAdminOnly]
    serializer_class = RolesSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    # permission_classes = [IsAdminOnly]
    serializer_class = StatusSerializer


class LoginView(APIView):
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            # if user.id_role == 1:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            response = Response({
                'refresh': str(refresh),
                'access': access,
                'id_role': user.id_role.id
            })
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                secure=True,
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax"
            )
            return response
        else:
            return Response({'error': f'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
