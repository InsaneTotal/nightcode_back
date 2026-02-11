from rest_framework import routers
from .views import UserViewSet, TypeDocumentViewSet, RolesViewSet, StatusViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'typedocuments', TypeDocumentViewSet)
router.register(r'roles', RolesViewSet)
router.register(r'status', StatusViewSet)

urlpatterns = router.urls
