from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import global_search_utils
# Create your views here.

class ProductSearch(APIView):
    def get(self, request):
        resp = global_search_utils(request)
        return Response(resp, status = resp['status_code'])