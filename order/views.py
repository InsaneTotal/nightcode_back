from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

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
    # permission_classes = [IsAdminOrReadOnly]


class TypeOrderStatusViewSet(viewsets.ModelViewSet):
    queryset = typeOrderStatus.objects.all()
    serializer_class = TypeOrderStatusSerializer
    permission_classes = [IsAdminOrReadOnly]


class TypeDrinkTablesViewSet(viewsets.ModelViewSet):
    queryset = typeDrinkTables.objects.all()
    serializer_class = TypeDrinkTablesSerializer
    # permission_classes = [IsAdminOrReadOnly]
    # Permite ingresar datos a la tabla de mesas, pero no eliminar ni modificar, solo lectura para los usuarios comunes y los permite a los administradores realizar cualquier acción.


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAdminOrReadOnly]


from django.contrib.auth import get_user_model


from rest_framework.permissions import AllowAny
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related(
        'id_users', 'id_mesa', 'id_payment', 'id_order_status'
    ).prefetch_related('details')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]   # Cambiado a AllowAny para permitir acceso sin autenticación
    def perform_create(self, serializer):
        User = get_user_model()
        user = User.objects.first()
        serializer.save(id_users=user)

    @action(detail=True, methods=["post"]) 
    def pay(self, request, pk=None):

        order = self.get_object()
        payment_method = request.data.get("id_payment")
        details = order.details.all()

        with transaction.atomic():

            for item in details:
                drink = item.drink

            if drink.amount < item.amount:
                return Response({
                    "error": f"No hay suficiente stock de {drink.name}"
                })

            drink.amount -= item.amount
            drink.save()

        # guardar método de pago
        if payment_method:
            order.id_payment_id = payment_method

        # cambiar estado a pagada
        order.id_order_status_id = 4
        order.save()

        return Response({"message": "Pago realizado y stock actualizado"})



class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all().select_related('id_drink', 'id_order')
    serializer_class = OrderDetailSerializer
    # permission_classes = [permissions.IsAuthenticated]