from django import forms
from shopifyapp.models import Product

class AddProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'discription', 'original_price' , 'discount_percentage', 'image', 'category']
