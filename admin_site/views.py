from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Genre
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from admin_site import serialisers
from rest_framework import status
from django.shortcuts import get_object_or_404


class CreationCategories(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        srz_data = serialisers.CreationCategoriesSerializers(data=request.data)
        if srz_data.is_valid():
            Genre.objects.create(name=srz_data.validated_data['name'])
            return Response({'message': f'{srz_data.validated_data["name"]} Category Has Been Successfully Added'},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CreationSubCategories(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        srz_data = serialisers.CreationSubCategoriesSerializers(data=request.data)
        if srz_data.is_valid():
            parent = get_object_or_404(Genre, id=srz_data.validated_data['id'])
            Genre.objects.create(name=srz_data.validated_data['name'], parent=parent)
            return Response({"message": "Your subcategory has been successfully created"},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
