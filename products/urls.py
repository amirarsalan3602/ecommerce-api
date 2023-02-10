from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductView.as_view(), name='all_products'),
    path('categories/', views.CategoriesView.as_view(), name='all_categories'),
    path('subcategories/<int:id>/', views.SubCategories.as_view(), name='sub_categories')
]
