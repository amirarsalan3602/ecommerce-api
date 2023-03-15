from django.urls import path
from admin_site import views

app_name = 'admin-site'
urlpatterns = [
    path("add_category/", views.CreationCategories.as_view(), name="add_category"),
    path("add_subcategory/", views.CreationSubCategories.as_view(), name="add_subcategory"),
    path("delete_category/<int:id>/", views.DeleteCategory.as_view(), name='delete_category'),
    path("delete_subcategory/<int:id>/", views.DeleteSubCategory.as_view(), name='delete_subcategory'),
    path("update_category/<int:id>/", views.UpdateCategory.as_view(), name='update_category'),
    path("update_subcategory/<int:id>/", views.UpdateSubCategory.as_view(), name='update_subcategory'),
    path("add_product/", views.CreationProduct.as_view(), name='add_product'),
]


