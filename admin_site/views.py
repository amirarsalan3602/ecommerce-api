from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Genre, DiscountModel
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from admin_site import serialisers
from rest_framework import status
from django.shortcuts import get_object_or_404

from products.serializers import UploadProductImageSerializer
from .tasks import all_bucket_objects_task
from rest_framework import viewsets


class CreationCategories(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        srz_data = serialisers.CreationCategoriesSerializers(data=request.data)
        if srz_data.is_valid():
            Genre.objects.create(name=srz_data.validated_data['name'])
            return Response({'message': f'{srz_data.validated_data["name"]} Category Has Been Successfully Added'},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CreationSubCategories(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        srz_data = serialisers.CreationSubCategoriesSerializers(data=request.data)
        if srz_data.is_valid():
            parent = get_object_or_404(Genre, id=srz_data.validated_data['id'])
            Genre.objects.create(name=srz_data.validated_data['name'], parent=parent)
            return Response({"message": "Your subcategory has been successfully created"},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategory(APIView):
    def post(self, request, id):
        try:
            obj = get_object_or_404(Genre, id=id, parent=None)
            obj.deactivate = True
            obj.save()
            obj = Genre.objects.filter(parent=id)
            for item in obj:
                item.deactivate = True
                item.save()
            return Response({'message': 'Delete Category successfully !'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Your Category Was Not Found !!'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCategory(APIView):
    def put(self, request, id):
        obj = Genre.objects.get(id=id, parent=None)
        srz_data = serialisers.CreationCategoriesSerializers(instance=obj, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSubCategory(APIView):
    def put(self, request, id):
        obj = Genre.objects.get(id=id)
        if obj.parent == None:
            return Response({'message': 'The selected object is a category! You must select a subcategory'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            srz_data = serialisers.CreationCategoriesSerializers(instance=obj, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteSubCategory(APIView):
    def post(self, request, id):
        try:
            obj = get_object_or_404(Genre, id=id)
            obj.deactivate = True
            obj.save()
            if obj.parent == None:
                return Response({'message': 'The selected object is a category! You must select a subcategory'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Delete Category successfully !'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Your Category Was Not Found !!'}, status=status.HTTP_400_BAD_REQUEST)


class CreationProduct(APIView):
    def post(self, request):
        srz_data = serialisers.CreationProductSerializers(data=request.data)
        if srz_data.is_valid():
            srz_data.create(srz_data.validated_data)
            return Response({'message': "Your product has been added !!"}, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadProductImageView(APIView):
    def post(self, request):
        srz_data = UploadProductImageSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.create(srz_data.validated_data)
            return Response(data={"the image product created !"})
        return Response(data=srz_data.errors, status=status.HTTP_404_NOT_FOUND)


class CreationDiscountView(APIView):
    def post(self, request):
        srz_data = serialisers.CreationDiscountSerializers(data=request.data)
        if srz_data.is_valid():
            srz_data.create(srz_data.validated_data)
            return Response({'message': 'Your discount has been successfully applied to the product.'},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
