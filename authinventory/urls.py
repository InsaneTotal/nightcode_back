from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DrinkViewSet, ImageUploadView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'drinks', DrinkViewSet)


urlpatterns = router.urls

# Endpoint único para subir imágenes
urlpatterns += [
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),
]
