from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from shopifyapp.models import Category , Product , Cart , CartItem
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from shopifyapp.forms import AddProductForm
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
class IndexPageView(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shopifyapp/index.html' , context={'products' : products})
    

class CreateProductView(LoginRequiredMixin , View):
    def get(self, request):
        context = {
            'form': AddProductForm()
        }                                                  
        return render(request, 'shopifyapp/add-product.html' , context)
    
    def post(self, request):    
        try :
            form = AddProductForm(request.POST , request.FILES)
            print(request.user)
        
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user  # Assigning the user to the product
                discount_price = instance.original_price * instance.discount_percentage / 100
                selling_price = instance.original_price - discount_price
                instance.selling_price = selling_price
                instance.save()

        except Exception as e :
            print(f'{type(e).__name__} : {e}')

        return redirect('shopify:home')
        

class CreateCategoryView(LoginRequiredMixin , View):
    flag = False
    def get(self, request):
        return render(request, 'shopifyapp/add-category.html')
    
    def post(self, request):
        flag = False
        try :
            category_name = request.POST.get('cname')
            category = Category(name = category_name)
            category.save()
            print("Product Added Successfully")
            flag =True

            return redirect('shopify:home')
        except Exception as e :
            flag =False
            print(f'{type(e).__name__} : {e}')
        return render(request, 'shopifyapp/add-category.html' , {'flag' : flag})
    


class ViewProduct(View) :

    def get(self , request , id):
        print(id)
        product = Product.objects.get(pk=id)
        return render(request , 'shopifyapp/view-product.html' , {'product':product})
    
        
    
class EditProduct(LoginRequiredMixin , View) :

    def get(self , request , id):
        product = Product.objects.get(pk=id)
        return render(request , 'shopifyapp/edit-product.html' , {'product':product})
    
    def post(self, request , id):    
        try :  
            # Fetching product and category from database
            db_product = Product.objects.get(pk=id)          
                                         
            # Calculation of discount and selling price
            original_price_user = float(request.POST.get("oprice").replace(",", ""))
            discount_percentage_user = float(request.POST.get("dprice").replace(",", ""))
            discount_price = (original_price_user * discount_percentage_user) / 100
            selling_price = original_price_user - discount_price

            # Updating database product object with new values
            db_product.name = request.POST.get("pname")
            db_product.discription = request.POST.get("discription")                                   
            db_product.original_price = original_price_user
            db_product.discount_percentage = discount_percentage_user
            db_product.selling_price = selling_price 
            db_product.image = request.FILES.get("image")

            # Save database product with new changes
            db_product.save()
            print("Product Updated Successfully")

            # Return redirect user to home page 
            return redirect('shopify:home')

        except Exception as e :
            print(f'{type(e).__name__} : {e}')
        return render(request, 'shopifyapp/add-product.html')
    

class DeleteProduct(LoginRequiredMixin , View) :

    def get(self , request , id):
        product = Product.objects.get(pk=id)
        return render(request, 'shopifyapp/delete.html', context={'product': product})
    
    def post(self, request , id):
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect('shopify:home')
    

class SearchProduct(View):

    def post(self, request):
        search = request.POST.get('search')
        search_list = Product.objects.filter(Q(name__icontains=search) | Q(category__name__icontains=search))
        return render(request, 'shopifyapp/searchlist.html', {'search_list': search_list})
    

class ElectronicsView(View):
    def get(self, request):
        product = Product.objects.filter(category__name = 'Electronics')
        print("Fetched Products :", product)
        return render(request , 'shopifyapp/electronics.html', {'product' : product} ) 
    

class ClothsView(View):
    def get(self, request):
        product = Product.objects.filter(category__name = 'Cloths')
        print("Fetched Products :", product)
        return render(request , 'shopifyapp/cloths.html', {'product' : product} ) 
    

class HomeAppliances(View):
    def get(self, request):
        product = Product.objects.filter(category__name = 'Home Appliances')
        print("Fetched Products :", product)
        return render(request , 'shopifyapp/home-appliances.html', {'product' : product} )
    

class GetProductByCreatedUser(LoginRequiredMixin, View):
    def get(self, request, id):
        product_list = Product.objects.filter(user__id=id)

        return render(request , 'shopifyapp/profile.html' , context={'products' : product_list})
    

class AddProductToCart(LoginRequiredMixin, View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)  
        user_cart , created = Cart.objects.get_or_create(user = request.user)  
        cart_item , created = CartItem.objects.get_or_create(cart = user_cart , product = product)

        if created :
            messages.success(request, 'Product added to cart successfully.')

        if not created :
            # if product already in cart then increase the quantity by 1
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Product quantity updated in cart.')

        return redirect ('shopify:view-product' , product.id)
    

class ViewCart(LoginRequiredMixin, View):
    def get(self, request):
        user_cart = get_object_or_404( Cart , user = request.user)
        cart_items = CartItem.objects.filter(cart = user_cart)
        context = {
            'cart' : user_cart ,
            'cart_items' : cart_items
            
        }

        return render(request , 'shopifyapp/view-cart.html' , context)
    

class UpdateCartItemQuantity(LoginRequiredMixin, View):
    def post(self, request, id):
        action = request.POST.get("action")  # "increase" or "decrease"
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=id, cart=cart)

        if action == "increase":
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantity increased.")
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, "Quantity decreased.")
            else:
                cart_item.delete()  # remove item if quantity goes to 0
                messages.success(request, "Item removed from cart.")

        return redirect("shopify:view-cart")
    
    