from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('products/', include('products.urls', namespace="products")),
    path('admin-site/', include('admin_site.urls', namespace="admin-site")),

]
