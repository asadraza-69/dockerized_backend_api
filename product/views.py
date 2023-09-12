from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .utils import global_search_utils
from .serializer import ProductSerializer,Product
# Create your views here.

class ProductSearch(APIView):
    def get(self, request):
        resp = global_search_utils(request)
        return Response(resp, status = resp['status_code'])

class ProductsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

