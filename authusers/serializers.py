from rest_framework import serializers
from .models import User, TypeDocument, Roles, Status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        # Encripta la contraseña usando el método set_password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            # El método save encripta la contraseña
            instance.set_password(password)
        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)
        instance.save()
        return instance


class TypeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDocument
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
