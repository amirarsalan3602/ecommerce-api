from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.core.validators import MinValueValidator, MaxValueValidator
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
    has_discount = models.BooleanField(default=False)
    discount = models.ForeignKey("DiscountModel", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='discount')

    def __str__(self):
        return f'{self.id} - {self.title} - {self.category}'


class ProductImagesModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product')


class CommentProductModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='pcomment')
    comment = models.TextField()
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='rcomment', null=True, blank=True)

    def __str__(self):
        return self.comment


class DiscountModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True, related_name='product')
    percent = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], blank=True, null=True)
    endprice = models.IntegerField(blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField(blank=True, null=True)
