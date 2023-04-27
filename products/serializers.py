from rest_framework import serializers
from products.models import ProductModel, CommentProductModel, ProductImagesModel, Genre, DiscountModel
from django.shortcuts import get_object_or_404
from rest_framework.serializers import SerializerMethodField


class UploadProductImageSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    image = serializers.ImageField()

    def create(self, validated_data):
        product = get_object_or_404(ProductModel, id=validated_data['product'])
        return ProductImagesModel.objects.create(product=product, image=validated_data['image'])


class ProductsSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True, many=True)
    images = SerializerMethodField()
    discount = SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = '__all__'

    def get_images(self, obj):
        return UploadProductImageSerializer(instance=obj.images.all(), many=True).data

    def get_discount(self, obj):
        if obj.has_discount:
            return DiscountSerializer(instance=DiscountModel.objects.get(id=obj.discount.id)).data
        else:
            return None


class CategoriesSerializers(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'parent']

    def get_parent(self, obj):
        return CategoriesSerializers(instance=obj.children.all(), many=True).data


class CommentProductSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    reply = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = CommentProductModel
        fields = ['id', "user", 'comment', 'is_reply', 'product', 'created', 'reply']

    def get_reply(self, obj):
        if not obj.is_reply:
            reply_queryset = CommentProductModel.objects.filter(reply_id=obj.id).order_by('created')
            reply_srz = self.__class__(instance=reply_queryset, many=True)
            return reply_srz.data

    def get_product(self, obj):
        return obj.product.title


class CreationCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentProductModel
        fields = ['id', 'comment']
        extra_kwargs = {
            "comment": {'required': True},
        }

    def create(self, validated_data):
        return CommentProductModel.objects.create(**validated_data)


class CreationReplySerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentProductModel
        fields = ['id', 'comment']
        extra_kwargs = {
            'id': {'required': True, 'read_only': False},
            'comment': {'required': True},
        }

    def create(self, validated_data):
        comment = get_object_or_404(CommentProductModel, id=validated_data['id'])
        return comment.rcomment.create(is_reply=True, comment=validated_data['comment'], product=comment.product,
                                       user=validated_data['user'])


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountModel
        fields = ['expired', 'endprice', 'percent']
