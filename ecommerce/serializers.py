from django.db.models import Avg
from rest_framework import serializers

from ecommerce.models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock_quantity", "category", "tags", "average_rating"]