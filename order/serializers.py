from rest_framework import serializers
from .models import (
    typeStatusTables,
    typeOrderStatus,
    typeDrinkTables,
    PaymentMethod,
    Order,
    OrderDetail,
)


class TypeStatusTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeStatusTables
        fields = '__all__'


class TypeOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeOrderStatus
        fields = '__all__'


class TypeDrinkTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeDrinkTables
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    id_drink = TypeDrinkTablesSerializer(read_only=True)
    id_drink_id = serializers.PrimaryKeyRelatedField(
        source='id_drink', queryset=typeDrinkTables.objects.all(), write_only=True
    )

    class Meta:
        model = OrderDetail
        fields = ['id', 'id_order', 'id_drink', 'id_drink_id', 'amount', 'unit_price']
        read_only_fields = ['id', 'id_drink']


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True, required=False)
    id_users = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'id_users', 'id_mesa', 'id_payment', 'date_order', 'id_order_status', 'total', 'details']
        read_only_fields = ['id', 'date_order', 'total']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['id_users'] = request.user
        order = Order.objects.create(**validated_data)
        total = 0
        for item in details_data:
            drink = item.get('id_drink')
            if isinstance(drink, typeDrinkTables):
                id_drink = drink
            else:
                id_drink = item.get('id_drink')
            amount = item.get('amount')
            unit_price = item.get('unit_price')
            OrderDetail.objects.create(id_order=order, id_drink=id_drink, amount=amount, unit_price=unit_price)
            total += (amount or 0) * float(unit_price or 0)
        order.total = total
        order.save()
        return order

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details_data is not None:

            instance.details.all().delete()
            total = 0
            for item in details_data:
                id_drink = item.get('id_drink')
                amount = item.get('amount')
                unit_price = item.get('unit_price')
                OrderDetail.objects.create(id_order=instance, id_drink=id_drink, amount=amount, unit_price=unit_price)
                total += (amount or 0) * float(unit_price or 0)
            instance.total = total
            instance.save()
        return instance
