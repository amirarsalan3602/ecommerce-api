from django.contrib import admin
from .models import Genre,oductM Prodel, CommentProductModel, ProductImagesModel,DiscountModel
from mptt.admin import MPTTModelAdmin

admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(ProductModel)
admin.site.register(CommentProductModel)
admin.site.register(ProductImagesModel)
admin.site.register(DiscountModel)
