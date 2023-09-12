from django.db import models
from django.conf import settings
from datetime import datetime
from authentication.utils import User
import os

# Create your models here.
def save_product_image(instance, filename):
    file_extension = os.path.splitext(filename)[1].lstrip('.')
    current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    target_dir = f'product_images/{instance.i_product.pk}'
    file_dir = os.path.join(settings.MEDIA_ROOT, target_dir)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir, 0o777)
    return os.path.join(target_dir, f'{current_datetime}.{file_extension}')
    
class Product(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product'
        ordering = ['pk']

    def __str__(self):
        return "%s - %s - %s" %(self.name,self.price,self.stock)

class ProductImages(models.Model):
    i_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_path = models.FileField(max_length=256, upload_to = save_product_image, null=True, blank=True)

    class Meta:
        db_table = 'product_image'
        ordering = ['pk']
    
    def __str__(self):
        return "%s" %(self.image_path.url)
    
class Cart(models.Model):
    i_user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='cart')
    
    class Meta:
        db_table = 'cart'

    def __str__(self):
        return str(self.i_user.email)
    
class CartItem(models.Model):
    i_cart = models.ForeignKey(Cart, on_delete= models.CASCADE , related_name= 'cart_items')
    i_product = models.ForeignKey(Product, on_delete= models.CASCADE)
    class Meta:
        db_table = 'cart_item'

    def __str__(self):
        return str(self.i_cart)
