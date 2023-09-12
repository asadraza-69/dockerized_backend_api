from django.urls import path
from . views import ProductSearch, ProductsListView
app_name = 'product'

urlpatterns = [
    path('search/', ProductSearch.as_view(), name='product_search'),
    path('', ProductsListView.as_view(), name='product_listview')
]