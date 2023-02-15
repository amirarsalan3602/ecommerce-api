from rest_framework import serializers
from products.models import Genre
from django.core.exceptions import ObjectDoesNotExist
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
            data = get_object_or_404(Genre,id=value)
            if str(type(data.parent)) == "<class 'NoneType'>":
                return value
        except Genre.DoesNotExist:
            raise serializers.ValidationError(" The value entered is incorrect ! ")

    def validate_name(self, value):
        if Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError(" This subcategory already exists ! ")
        return value
