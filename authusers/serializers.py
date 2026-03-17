from rest_framework import serializers
from .models import User, TypeDocument, Roles, Status


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='id_role.name', read_only=True)

    class Meta:
        model = User
        # Excluir 'groups' y 'user_permissions' de los campos
        fields = [
            field.name for field in User._meta.fields
            if field.name not in ('groups', 'user_permissions')
        ] + [
            field.name for field in User._meta.many_to_many
            if field.name not in ('groups', 'user_permissions')
        ] + ['role_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['is_active'] = True
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


class CurrentUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'role']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_role(self, obj):
        if not obj.id_role:
            return None
        return {
            'id': obj.id_role.id,
            'name': obj.id_role.name,
        }


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
