from rest_framework import serializers
from products.models import ProductModel


class ProductsSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


class CategoriesSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.CharField()
