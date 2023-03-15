from django.contrib import admin
from .models import Genre,ProductModel,CommentProductModel
from mptt.admin import MPTTModelAdmin

admin.site.register(Genre,MPTTModelAdmin)
admin.site.register(ProductModel)
admin.site.register(CommentProductModel)

