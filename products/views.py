from rest_framework.views import APIView
from .models import ProductModel, Genre, CommentProductModel, ProductImagesModel
from .serializers import ProductsSerializers, CategoriesSerializers, CommentProductSerializers, \
    CreationCommentSerializers, CreationReplySerializers, UploadProductImageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from celery import shared_task
from rest_framework import viewsets


# List of all product
class ProductViewSet(viewsets.ViewSet):
    queryset = ProductModel.objects.all()

    def list(self, request):
        srz_data = ProductsSerializers(instance=self.queryset, many=True).data
        return Response(data=srz_data, status=status.HTTP_200_OK)


# List of all categories and SubCategory
class CategoriesView(APIView):
    def get(self, request):
        # all_categories = Genre.objects.filter(parent__isnull=True)
        all_categories = Genre.objects.filter(parent=None, deactivate=False)
        srz_data = CategoriesSerializers(instance=all_categories, many=True).data
        return Response(data=srz_data)


# # list of sub Categories Based on ID Category
# class SubCategoriesView(APIView):
#     def get(self, request, id):
#         # Category ID to get the relevant subcategories
#         sub_cat = Genre.objects.filter(parent=id, deactivate=False)
#         if sub_cat:
#             srz_data = CategoriesSerializers(instance=sub_cat, many=True)
#             return Response(data=srz_data.data, status=status.HTTP_200_OK)
#         return Response(data={})

class CommentProductView(APIView):

    def get(self, request, id):
        # An ID to get a product
        product = get_object_or_404(ProductModel, id=id)
        comments = CommentProductModel.objects.filter(product=product, is_reply=False, reply=None)
        srz_data = CommentProductSerializers(instance=comments, many=True)
        return Response(data=srz_data.data)


class CreationCommentView(APIView):
    def post(self, request, id):
        # An ID to get a product
        srz_data = CreationCommentSerializers(data=request.POST)
        if srz_data.is_valid():
            srz_data.validated_data['user'] = request.user
            srz_data.validated_data['reply'] = None
            srz_data.validated_data['product'] = get_object_or_404(ProductModel, id=id)
            srz_data.create(srz_data.validated_data)
            return Response(data=srz_data.data, status=status.HTTP_201_CREATED)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CreationReplyView(APIView):
    def post(self, request):
        srz_data = CreationReplySerializers(data=request.data)
        if srz_data.is_valid():
            srz_data.validated_data['user'] = request.user
            srz_data.create(srz_data.validated_data)
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
