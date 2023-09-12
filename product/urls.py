from django.urls import path
from . views import ProductSearch
app_name = 'product'

urlpatterns = [
    path('search/', ProductSearch.as_view(), name='product_search')
]