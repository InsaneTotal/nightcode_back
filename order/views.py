from rest_framework import viewsets, permissions
from .models import (
	typeStatusTables,
	typeOrderStatus,
	typeDrinkTables,
	PaymentMethod,
	Order,
	OrderDetail,
)
from .serializers import (
	TypeStatusTablesSerializer,
	TypeOrderStatusSerializer,
	TypeDrinkTablesSerializer,
	PaymentMethodSerializer,
	OrderSerializer,
	OrderDetailSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user and request.user.is_staff


class TypeStatusTablesViewSet(viewsets.ModelViewSet):
	queryset = typeStatusTables.objects.all()
	serializer_class = TypeStatusTablesSerializer
	permission_classes = [IsAdminOrReadOnly]


class TypeOrderStatusViewSet(viewsets.ModelViewSet):
	queryset = typeOrderStatus.objects.all()
	serializer_class = TypeOrderStatusSerializer
	permission_classes = [IsAdminOrReadOnly]


class TypeDrinkTablesViewSet(viewsets.ModelViewSet):
	queryset = typeDrinkTables.objects.all()
	serializer_class = TypeDrinkTablesSerializer
	permission_classes = [IsAdminOrReadOnly]


class PaymentMethodViewSet(viewsets.ModelViewSet):
	queryset = PaymentMethod.objects.all()
	serializer_class = PaymentMethodSerializer
	permission_classes = [IsAdminOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all().select_related('id_users', 'id_mesa', 'id_payment', 'id_order_status').prefetch_related('details')
	serializer_class = OrderSerializer
	# permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(id_users=self.request.user)
		else:
			serializer.save()


class OrderDetailViewSet(viewsets.ModelViewSet):
	queryset = OrderDetail.objects.all().select_related('id_drink', 'id_order')
	serializer_class = OrderDetailSerializer
	# permission_classes = [permissions.IsAuthenticated]
