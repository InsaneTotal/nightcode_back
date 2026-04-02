from io import BytesIO
from urllib.parse import urlencode

import qrcode
from django.conf import settings
from django.db.models import Sum
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from authusers.permissions import IsAdminOrIsWaitressOrIsBartender
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
    TopDrinkTodaySerializer,
)

class TypeStatusTablesViewSet(viewsets.ModelViewSet):
    queryset = typeStatusTables.objects.all()
    serializer_class = TypeStatusTablesSerializer


class TypeOrderStatusViewSet(viewsets.ModelViewSet):
    queryset = typeOrderStatus.objects.all()
    serializer_class = TypeOrderStatusSerializer


class TypeDrinkTablesViewSet(viewsets.ModelViewSet):
    queryset = typeDrinkTables.objects.all()
    serializer_class = TypeDrinkTablesSerializer

    def _ensure_tokens_for_queryset(self, queryset):
        tables = list(queryset)
        for table in tables:
            if not table.qr_token:
                table.ensure_qr_token()
        return tables

    def list(self, request, *args, **kwargs):
        tables = self._ensure_tokens_for_queryset(self.filter_queryset(self.get_queryset()))
        serializer = self.get_serializer(tables, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        table = self.get_object()
        if not table.qr_token:
            table.ensure_qr_token()
            table.refresh_from_db(fields=['qr_token'])
        serializer = self.get_serializer(table)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='call-waiter', permission_classes=[permissions.AllowAny])
    def call_waiter(self, request, pk=None):
        token = str(request.data.get('token', '')).strip()
        if not token:
            return Response(
                {'detail': 'Falta token de mesa.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        table = typeDrinkTables.objects.filter(pk=pk).first()
        if table is None:
            return Response(
                {'detail': 'Mesa no encontrada.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if settings.CALL_WAITER_STRICT_TOKEN and (not table.qr_token or token != table.qr_token):
            return Response(
                {'detail': 'Token de mesa invalido.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        pending_status = typeStatusTables.objects.filter(
            Q(name__iexact='Pendiente') | Q(name__icontains='llam')
        ).first()
        if pending_status is None:
            return Response(
                {'detail': 'No hay estado configurado para llamado de mesero.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        table.status = pending_status
        table.save(update_fields=['status'])

        return Response({'detail': 'Mesero llamado con exito'}, status=status.HTTP_200_OK)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related(
        'id_users', 'id_mesa', 'id_payment', 'id_order_status'
    ).prefetch_related('details')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrIsWaitressOrIsBartender]

    def perform_create(self, serializer):
        User = get_user_model()
        user = User.objects.first()
        serializer.save(id_users=user)

    @action(detail=False, methods=['get'], url_path='top-drinks-today')
    def top_drinks_today(self, request):
        today = timezone.localdate()
        top_drinks = (
            OrderDetail.objects.filter(
                id_order__date_order__date=today,
                drink__isnull=False,
            )
            .values('drink_id', 'drink__name')
            .annotate(total_units_sold=Sum('amount'))
            .order_by('-total_units_sold', 'drink__name')[:3]
        )

        serializer = TopDrinkTodaySerializer(
            [
                {
                    'drink_id': item['drink_id'],
                    'drink_name': item['drink__name'],
                    'total_units_sold': item['total_units_sold'] or 0,
                }
                for item in top_drinks
            ],
            many=True,
        )
        return Response(serializer.data)


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


class DownloadTableQRView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrIsWaitressOrIsBartender]

    def get(self, request, table_id: int):
        table = get_object_or_404(typeDrinkTables, pk=table_id)

        try:
            token = table.ensure_qr_token()
            base_url = settings.FRONTEND_MENU_BASE_URL.rstrip('/')
            query = urlencode({'mesa': table.id, 'token': token})
            menu_url = f"{base_url}?{query}"

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(menu_url)
            qr.make(fit=True)

            image = qr.make_image(fill_color='black', back_color='white')
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            response = HttpResponse(buffer.getvalue(), content_type='image/png')
            response['Content-Disposition'] = (
                f'attachment; filename="mesa-{table.id}-qr.png"'
            )
            return response
        except Exception:
            return Response(
                {'detail': 'Error generating QR image.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
