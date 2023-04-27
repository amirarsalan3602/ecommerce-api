from rest_framework import serializers
from lib.DiscountCalculator import discount_calculator, decrease_percentage
from lib.find_Date import find_date
from accounts.models import User
from products.models import Genre, ProductModel, DiscountModel

from django.shortcuts import get_object_or_404


class CreationCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', ]
        extra_kwargs = {
            'name': {'required': True, }
        }


class CreationSubCategoriesSerializers(serializers.Serializer):
    id = serializers.IntegerField(required=True, )
    name = serializers.CharField(required=True)

    def validate_id(self, value):
        try:
            data = get_object_or_404(Genre, id=value)
            if str(type(data.parent)) == "<class 'NoneType'>":
                return value
        except Genre.DoesNotExist:
            raise serializers.ValidationError(" The value entered is incorrect ! ")

    def validate_name(self, value):
        if Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError(" This subcategory already exists ! ")
        return value


class CreationProductSerializers(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    category = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)

    def create(self, validated_data):
        title = validated_data['title']
        description = validated_data['description']
        price = validated_data['price']
        user = User.objects.get(id=validated_data['user'])
        category = get_object_or_404(Genre, name=validated_data['category'])
        product = ProductModel.objects.create(user=user, title=title, description=description,
                                              price=price)
        product.category.add(category.id, category.parent.id)
        product.save()
        return None


class CreationDiscountSerializers(serializers.Serializer):
    product_id = serializers.IntegerField()
    percent = serializers.IntegerField(required=False)
    endprice = serializers.IntegerField(required=False)
    expired = serializers.CharField()

    def create(self, validated_data):
        try:
            try:
                if validated_data['percent']:
                    product = ProductModel.objects.get(id=validated_data['product_id'])
                    expired = find_date(validated_data['expired'])
                    end_price = discount_calculator(product.price, discount_percent=validated_data['percent'])
                    return DiscountModel.objects.create(product=product, percent=validated_data['percent'],
                                                        endprice=int(end_price),
                                                        expired=expired)
            except:

                if validated_data['endprice']:
                    product = ProductModel.objects.get(id=validated_data['product_id'])
                    percent = decrease_percentage(p1=product.price, p2=validated_data['endprice'])
                    expired = find_date(validated_data['expired'])
                    return DiscountModel.objects.create(product=product, percent=percent,
                                                        endprice=validated_data['endprice'],
                                                        expired=expired)
        except:
            if validated_data['percent'] & validated_data['endprice']:
                raise ValueError('You can only send one of the two items percent or endprice !!')
