from django.urls import path
from shopifyapp.views import IndexPageView , CreateProductView , CreateCategoryView , ViewProduct , EditProduct , DeleteProduct , SearchProduct , ElectronicsView , ClothsView , GetProductByCreatedUser , HomeAppliances , AddProductToCart , ViewCart , UpdateCartItemQuantity

urlpatterns = [
    path('', IndexPageView.as_view(), name='home'),
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('view-product/<int:id>/', ViewProduct.as_view(), name='view-product'),
    path('edit-product/<int:id>/', EditProduct.as_view(), name='edit-product'),
    path('delete-product/<int:id>/', DeleteProduct.as_view(), name='delete-product'),
    path('search-product/', SearchProduct.as_view(), name='search-product'),
    path('electronics-product/', ElectronicsView.as_view(), name='electronics-product'),
    path('cloths-product/', ClothsView.as_view(), name='cloths-product'),
    path('home-appliances-product/', HomeAppliances.as_view(), name='home-appliances-product'),
    path('user-product/<int:id>/', GetProductByCreatedUser.as_view(), name='user-product'),
    path('add-to-cart/<int:id>/', AddProductToCart.as_view(), name='add-to-cart'),
    path('view-cart/', ViewCart.as_view(), name='view-cart'),
    path("update-cart-item/<int:id>/", UpdateCartItemQuantity.as_view(), name="update-cart-item"),

]
 
