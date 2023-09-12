from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import (generics, permissions, status)
from rest_framework.response import Response
from .utils import global_search_utils
from .serializer import ProductSerializer,Product
from .models import CartItem, Cart
from django.db import transaction

# Create your views here.

class ProductSearch(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        resp = global_search_utils(request)
        return Response(resp, status = resp['status_code'])

class ProductsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class AddToCart(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        response = {'status':False,'status_code':status.HTTP_200_OK,'message':None, 'data' : None}
        product_id = kwargs['id']
        product_qs = Product.objects.filter(id=product_id)
        if product_qs.exists():
            product_obj = product_qs.first()
            with transaction.atomic():
                cart_obj, created = Cart.objects.get_or_create(i_user =  request.user)
                CartItem.objects.create(i_cart=cart_obj,i_product=product_obj)
                response['status'] = True
                response['status_code'] = status.HTTP_200_OK
                response['message'] = 'Product added successfully'
        else:
            response['status'] = False
            response['status_code'] = status.HTTP_404_NOT_FOUND
            response['message'] = 'Product not found'
        return Response(response , status = response['status_code'])