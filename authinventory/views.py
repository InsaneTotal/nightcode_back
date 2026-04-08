from rest_framework import viewsets
from authusers.permissions import IsAdminOrIsWaitressOrIsBartender
from .serializers import CategorySerializer, DrinkSerializer
from .models import Category, Drink
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from rest_framework.permissions import AllowAny


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            image = serializer.validated_data['image']
            return Response({'url': request.build_absolute_uri(image.url)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrIsWaitressOrIsBartender]


class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all().select_related('category')
    serializer_class = DrinkSerializer
    # permission_classes = [IsAdminOrIsWaitressOrIsBartender]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
