from django.db import models
from django.conf import settings
from authinventory.models import Drink


class typeStatusTables(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"


class typeOrderStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "estado nombre"
        verbose_name_plural = "estado nombres"


class typeDrinkTables(models.Model):
    name = models.CharField(max_length=255, unique=True)
    status = models.ForeignKey(
        typeStatusTables,
        on_delete=models.PROTECT,
        related_name="drinks",
        db_column="id_Status"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de bebida"
        verbose_name_plural = "Tipos de bebidas"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"


class Order(models.Model):
    id_users = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        db_column="id_users"
    )
    id_mesa = models.ForeignKey(
        typeDrinkTables,
        on_delete=models.PROTECT,
        related_name="orders",
        db_column="id_mesa"
    )
    id_payment = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        related_name="orders",
        db_column="id_payment",
        null=True,
        blank=True
    )
    date_order = models.DateTimeField(auto_now_add=True)
    id_order_status = models.ForeignKey(
        typeOrderStatus,
        on_delete=models.PROTECT,
        related_name="orders",
        db_column="id_order_status"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden {self.pk} - Usuario {self.id_users_id} - {self.total}"

    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"


class OrderDetail(models.Model):
    id_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="details",
        db_column="id_order"
    )

    id_drink = models.ForeignKey(
        typeDrinkTables,
        on_delete=models.PROTECT,
        related_name="order_details",
        db_column="id_drink",
        null=True,
        blank=True
    )

    drink = models.ForeignKey(
        Drink,
        on_delete=models.PROTECT,
        related_name="order_details_real",
        null=True,
        blank=True
    )

    amount = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.pk} - Orden {self.id_order_id} - {self.amount}"
    class Meta:
        verbose_name = "Detalle de orden"
        verbose_name_plural = "Detalles de orden"