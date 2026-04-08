from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
from .models import Category, Drink


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Si es un string base64
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            return super().to_internal_value(data)
        # Si es un archivo (InMemoryUploadedFile o similar)
        if hasattr(data, 'read') and hasattr(data, 'name'):
            return super().to_internal_value(data)
        # Si es None o vacío y no es requerido
        if data in (None, ''):
            return None
        raise serializers.ValidationError(
            'Formato de imagen no soportado. Debe ser archivo o base64.')


class ImageUploadSerializer(serializers.Serializer):
    image = Base64ImageField(required=True)

    def to_representation(self, instance):
        # instance es el archivo guardado (ruta relativa)
        request = self.context.get('request')
        if request:
            return {
                'url': request.build_absolute_uri(instance.url)
            }
        return {'url': instance.url}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        value = value.strip()
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Esta categoría ya existe")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        if not name:
            raise serializers.ValidationError(
                "El nombre de la categoría es requerido.")
        return Category.objects.create(**validated_data)


class DrinkSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', read_only=True)
    url_img = Base64ImageField(required=False)

    class Meta:
        model = Drink
        fields = '__all__'
