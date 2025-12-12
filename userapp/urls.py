from django.urls import path
from userapp.views import UserRegisterView , edit_profile , delete_profile
from django.contrib.auth import views as  auth_views
app_name = "userapp"


urlpatterns = [
    path('register/<str:role>/', UserRegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),

]

 