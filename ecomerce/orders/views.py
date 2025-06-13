from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar pedidos
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Solo mostrar pedidos del usuario autenticado"""
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Crear nuevo pedido"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Retornar la orden creada con el serializer de lectura
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """Cancelar pedido"""
        order = self.get_object()
        
        if not order.can_be_cancelled:
            return Response(
                {'error': f'No se puede cancelar un pedido en estado {order.get_status_display()}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restaurar stock usando transacción
        with transaction.atomic():
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()
            
            order.status = 'cancelled'
            order.save()
        
        return Response({'message': 'Pedido cancelado exitosamente'})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Resumen de pedidos del usuario"""
        orders = self.get_queryset()
        
        summary = {
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'processing_orders': orders.filter(status='processing').count(),
            'delivered_orders': orders.filter(status='delivered').count(),
            'cancelled_orders': orders.filter(status='cancelled').count(),
        }
        
        return Response(summary)