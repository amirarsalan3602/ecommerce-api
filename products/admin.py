from django.contrib import admin
from .models import Genre, CommentProductModel, ProductImagesModel, DiscountModel, ProductModel
from mptt.admin import MPTTModelAdmin

admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(ProductModel)
admin.site.register(CommentProductModel)
admin.site.register(ProductImagesModel)
admin.site.register(DiscountModel)
