from rest_framework import serializers

from products.models import ProductModel, Genre


class ProductsSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','name', 'parent']
        # fields = "__all__"


# class SubCategoriesSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ['id']

