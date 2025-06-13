from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status', 'shipping_address', 
            'phone', 'notes', 'created_at', 'updated_at', 'items'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'notes', 'items']

    def validate_items(self, value):
        """Validar que haya al menos un artículo"""
        if not value:
            raise serializers.ValidationError("El pedido debe tener al menos un artículo.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(
            user=self.context['request'].user,
            total_amount=0,  # Se calculará después
            **validated_data
        )

        total_amount = 0
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f'Producto con ID {item_data["product_id"]} no existe.'
                )
            
            # Verificar que el producto esté activo
            if not product.is_active:
                raise serializers.ValidationError(
                    f'El producto {product.name} no está disponible.'
                )
            
            # Verificar stock disponible
            if product.stock < item_data['quantity']:
                raise serializers.ValidationError(
                    f'Stock insuficiente para {product.name}. '
                    f'Stock disponible: {product.stock}'
                )
            
            # Crear item de orden
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price  # Usar precio actual del producto
            )
            
            # Actualizar stock
            product.stock -= item_data['quantity']
            product.save()
            
            total_amount += order_item.total

        order.total_amount = total_amount
        order.save()
        
        return order