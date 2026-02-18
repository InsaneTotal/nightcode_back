from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DrinkViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'drinks', DrinkViewSet)

urlpatterns = router.urls
