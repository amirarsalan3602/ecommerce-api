from django.db import models
from mptt.models import TreeForeignKey, MPTTModel

from accounts.models import User


class Genre(MPTTModel):
    name = models.CharField(max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True, related_name='children')

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField(Genre)
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.title} - {self.category}'
