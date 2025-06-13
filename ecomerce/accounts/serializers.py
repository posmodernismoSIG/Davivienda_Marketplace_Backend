from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer para crear usuarios"""
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone', 'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
    def create(self, validated_data):
        """Crear usuario removiendo password_confirm"""
        validated_data.pop('password_confirm', None)
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    """Serializer para mostrar información del usuario"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    has_complete_profile = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'birth_date', 'address', 'full_name', 
            'has_complete_profile', 'date_joined', 'is_verified'
        ]
        read_only_fields = ['date_joined', 'is_verified']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar perfil de usuario"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'birth_date', 'address'
        ]
    
    def validate_email(self, value):
        """Validar que el email sea único"""
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value