from .models import Product
from django.db.models import Q
from django.urls import reverse


def global_search_utils(request):
    resp = {}
    keyword = request.query_params.get('keyword')
    product_qs = Product.objects.filter(
        Q(name__icontains = keyword)|
        Q(stock__icontains = int(keyword))|
        Q(price__icontains = int(keyword))|
        Q(description__icontains = keyword)
        )
    product_list = list(map(
        lambda product: {
            'pk' : product.pk,
            'name' : product.name,
            'description' : product.description,
            'stock' : product.stock,
            'price' : product.price,
            # 'url' : reverse('user_management:get_profile_id',args=[user.profile.pk]),
            }, product_qs))
    
    if not product_list:
        resp = {"status_code":200,"message":"No Search Results",'status' : False, 'data'  :{}}
    else:
        resp = {"status_code":200,"message":"Search Results",'status' : True, 'data'  :{"product": product_list}}

    return resp