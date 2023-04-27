from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductView.as_view(), name='all_products'),
    # list All products
    path('categories/', views.CategoriesView.as_view(), name='all_categories'),
    # list of categories
    path('comments/<int:id>/', views.CommentProductView.as_view(), name='all_comment'),
    # comments list based on ID Product
    path('add_comment/<int:id>/', views.CreationCommentView.as_view(), name='add_comment'),
    # creation a comment by ID product
    path('add_reply/', views.CreationReplyView.as_view(), name='add_reply'),


]
