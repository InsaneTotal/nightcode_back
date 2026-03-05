from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Category, Drink
from .serializers import CategorySerializer, DrinkSerializer

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [IsAdminUser] 

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    #permission_classes = [IsAdminUser] 


