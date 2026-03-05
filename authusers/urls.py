from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import LoginView, UserViewSet, TypeDocumentViewSet, RolesViewSet, StatusViewSet
from .views import RefreshTokenView

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'typedocuments', TypeDocumentViewSet)
router.register(r'roles', RolesViewSet)
router.register(r'status', StatusViewSet)


custom_urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cookie/refresh/', RefreshTokenView.as_view(),
         name='cookie_token_refresh'),
]

urlpatterns = router.urls + custom_urlpatterns
