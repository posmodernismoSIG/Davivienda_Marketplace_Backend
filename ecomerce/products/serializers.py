from rest_framework import serializers
from .models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        # Asegurar que el usuario no puede hacer review al mismo producto dos veces
        user = self.context['request'].user
        product = validated_data['product']
        
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                "Ya has hecho una reseña para este producto."
            )
        
        return Review.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'category_id',
            'stock', 'image', 'is_active', 'created_at', 'updated_at',
            'reviews', 'average_rating', 'is_in_stock'
        ]

    def validate_price(self, value):
        """Validar que el precio sea mayor que cero"""
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value

    def validate_stock(self, value):
        """Validar que el stock no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def validate_category_id(self, value):
        """Validar que la categoría existe"""
        try:
            Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("La categoría especificada no existe.")
        return value

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer más liviano para listado de productos"""
    category = serializers.StringRelatedField()
    average_rating = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'stock', 'image', 
            'average_rating', 'is_in_stock'
        ]