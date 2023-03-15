from django.db import models
from mptt.models import TreeForeignKey, MPTTModel

from accounts.models import User


class Genre(MPTTModel):
    name = models.CharField(max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    deactivate = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['name']

    def display(self):
        if self.deactivate:
            return None
        return self.deactivate

    def __str__(self):
        return f'{self.name}'


class ProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Genre, related_name='product')
    title = models.CharField(max_length=256)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.id} - {self.title} - {self.category}'


class CommentProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='pcomment')
    comment = models.TextField()
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='rcomment', null=True, blank=True)

    def __str__(self):
        return self.comment
