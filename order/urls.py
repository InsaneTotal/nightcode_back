from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    TypeStatusTablesViewSet,
    TypeOrderStatusViewSet,
    TypeDrinkTablesViewSet,
    PaymentMethodViewSet,
    OrderViewSet,
    OrderDetailViewSet,
    DownloadTableQRView,
)

router = DefaultRouter()
router.register(r'status-tables', TypeStatusTablesViewSet)
router.register(r'order-status', TypeOrderStatusViewSet)
router.register(r'drink-tables', TypeDrinkTablesViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)

urlpatterns = [
    path('tables/<int:table_id>/qr/download/', DownloadTableQRView.as_view(), name='table-qr-download'),
    path('tables/<int:pk>/call-waiter/', TypeDrinkTablesViewSet.as_view({'post': 'call_waiter'}), name='table-call-waiter'),
] + router.urls
