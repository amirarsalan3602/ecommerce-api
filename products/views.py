from rest_framework.views import APIView
from .models import ProductModel, Genre
from .serializers import ProductsSerializers, CategoriesSerializers
from rest_framework.response import Response
from rest_framework import status


# List of all product
class ProductView(APIView):
    def get(self, request):
        products = ProductModel.objects.all()
        srz_data = ProductsSerializers(instance=products, many=True).data
        return Response(data=srz_data, status=status.HTTP_200_OK)


# List of all categories
class CategoriesView(APIView):
    def get(self, request):
        # all_categories = Genre.objects.filter(parent__isnull=True)
        all_categories = Genre.objects.filter(parent=None, deactivate=False)
        srz_data = CategoriesSerializers(instance=all_categories, many=True).data
        return Response(data=srz_data)


# list of sub Categories Based on ID Category
class SubCategories(APIView):
    def get(self, request, id):
        sub_cat = Genre.objects.filter(parent=id, deactivate=False)
        if sub_cat:
            srz_data = CategoriesSerializers(instance=sub_cat, many=True)
            return Response(data=srz_data.data, status=status.HTTP_200_OK)
        return Response(data={})
