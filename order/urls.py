from rest_framework.routers import DefaultRouter
from .views import (
    TypeStatusTablesViewSet,
    TypeOrderStatusViewSet,
    TypeDrinkTablesViewSet,
    PaymentMethodViewSet,
    OrderViewSet,
    OrderDetailViewSet,
)

router = DefaultRouter()
router.register(r'status-tables', TypeStatusTablesViewSet)
router.register(r'order-status', TypeOrderStatusViewSet)
router.register(r'drink-tables', TypeDrinkTablesViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)

urlpatterns = router.urls