from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileUpdateSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.GenericViewSet):
    """
    ViewSet para gestión de perfil de usuario
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Retorna el usuario actual"""
        return self.request.user
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], 
            serializer_class=UserProfileUpdateSerializer)
    def update_profile(self, request):
        """Actualizar perfil del usuario"""
        serializer = self.get_serializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Retornar datos actualizados
        response_serializer = UserSerializer(request.user)
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['post'])
    def verify_profile(self, request):
        """Verificar si el perfil está completo"""
        user = request.user
        
        missing_fields = []
        required_fields = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'phone': 'Teléfono',
            'address': 'Dirección'
        }
        
        for field, label in required_fields.items():
            if not getattr(user, field):
                missing_fields.append(label)
        
        return Response({
            'is_complete': len(missing_fields) == 0,
            'missing_fields': missing_fields,
            'completion_percentage': round(
                ((len(required_fields) - len(missing_fields)) / len(required_fields)) * 100, 2
            )
        })