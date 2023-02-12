from django.urls import path
from admin_site import views

app_name = 'admin-site'
urlpatterns = [
            path("add_category/",views.CreationCategories.as_view(),name="add_category"),
]
