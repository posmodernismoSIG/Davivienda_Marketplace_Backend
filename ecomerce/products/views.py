from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Product, Category, Review
from .serializers import (
    ProductSerializer, 
    ProductListSerializer, 
    CategorySerializer, 
    ReviewSerializer
)
from .filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar categorías
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """
        Solo administradores pueden crear, actualizar o eliminar categorías
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar productos
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'created_at', 'name', 'stock']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Usar serializer más liviano para listado
        """
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        """
        Solo administradores pueden crear, actualizar o eliminar productos
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk=None):
        """
        Endpoint para agregar reseña a un producto
        """
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Endpoint para productos destacados
        """
        featured_products = self.queryset.filter(stock__gt=0)[:8]
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Endpoint para productos con stock bajo (solo admin)
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para acceder a esta información'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        low_stock_products = Product.objects.filter(stock__lte=5, is_active=True)
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)