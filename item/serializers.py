from rest_framework import serializers

from .models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_detail = CategorySerializer(source='category', read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = (
            'id', 'category', 'category_detail', 'name', 'description',
            'price', 'image', 'is_sold', 'created_by', 'created_at',
        )
        read_only_fields = ('created_by', 'created_at')
