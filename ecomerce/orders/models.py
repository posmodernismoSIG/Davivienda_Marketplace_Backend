from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.core.validators import MinValueValidator

# Obtener el modelo de usuario personalizado
User = get_user_model()

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name="Usuario"
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Monto total"
    )
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='pending',
        verbose_name="Estado"
    )
    shipping_address = models.TextField(verbose_name="Dirección de envío")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    notes = models.TextField(blank=True, verbose_name="Notas adicionales")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.id} - {self.user.username}'

    @property
    def can_be_cancelled(self):
        """Determina si el pedido puede ser cancelado"""
        return self.status in ['pending', 'processing']

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Pedido"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio unitario"
    )  # Precio al momento de la compra

    class Meta:
        verbose_name = "Artículo del pedido"
        verbose_name_plural = "Artículos del pedido"

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    @property
    def total(self):
        """Calcula el total del artículo"""
        return self.quantity * self.price