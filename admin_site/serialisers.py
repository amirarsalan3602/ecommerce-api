from rest_framework import serializers
from products.models import Genre


class CreationCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', ]
        extra_kwargs = {
            'name': {'required': True,}
        }
