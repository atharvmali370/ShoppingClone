from django.db import models
from userapp.models import User

# Create your models here.
class Category (models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    discription = models.TextField()
    original_price = models.FloatField()
    discount_percentage = models.IntegerField()
    selling_price = models.FloatField()
    image = models.ImageField(upload_to='media')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"  
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"
    
    def get_total_cart_price(self):
        return sum(item.get_total_item_price() for item in self.cartitem_set.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name} in {self.cart.user.username}'s Cart"
    
    def get_total_item_price(self):
        return self.product.selling_price * self.quantity
    
    
