from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Category, Drink
from .serializers import CategorySerializer, DrinkSerializer
from authusers.permissions import IsAdminOrIsWaitressOrIsBartender

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrIsWaitressOrIsBartender]

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    # permission_classes = [IsAdminOrIsWaitressOrIsBartender]
    parser_classes = [JSONParser, MultiPartParser, FormParser] 


