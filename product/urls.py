from django.urls import path
from . views import (ProductSearch, ProductsListView, AddToCart)
app_name = 'product'

urlpatterns = [
    path('search/', ProductSearch.as_view(), name='product_search'),
    path('cart_item/<int:id>/', AddToCart.as_view(), name='cart_item'),
    path('', ProductsListView.as_view(), name='product_listview')
]