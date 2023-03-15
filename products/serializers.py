from abc import ABC

from rest_framework import serializers
from products.models import ProductModel, CommentProductModel
from django.shortcuts import get_object_or_404


class ProductsSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = ProductModel
        fields = '__all__'


class CategoriesSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parent = serializers.CharField()


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
