from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Genre
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from admin_site import serialisers
from rest_framework import status


class CreationCategories(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request):
        srz_data = serialisers.CreationCategoriesSerializers(data=request.data)
        if srz_data.is_valid():
            Genre.objects.create(name=srz_data.validated_data['name'])
            return Response({'message': f'{srz_data.validated_data["name"]} Category Has Been Successfully Added'},
                            status=status.HTTP_201_CREATED)
        return Response(srz_data.errors)
