from django.shortcuts import render, redirect , get_object_or_404
from django.views import View
from userapp.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from userapp.models import UserProfile
from django.contrib.auth import logout
from django.contrib import messages
from userapp.forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash


class UserRegisterView(View):
    def get(self, request, role):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, 'userapp/register.html', context)

    def post(self, request, role):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if role == 'seller':
                instance.is_seller = True
            elif role == 'buyer':
                instance.is_buyer = True
            instance.save()
            
        return redirect('shopify:home')



# Edit Profile View
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user fields
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Update profile fields
            form.save()
            
            # ✅ Keep user logged in after username change
            update_session_auth_hash(request, request.user)

            messages.success(request, "Profile updated successfully ✅")
            return redirect("shopify:home")
    else:
        form = UserProfileForm(instance=profile, initial={
            'username': request.user.username,
            'email': request.user.email
        })

    return render(request, "userapp/edit_profile.html", {"form": form})

       


# Delete Profile View
@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)   # log them out before deletion
        user.delete()
        return redirect("shopify:home")

    return render(request, "userapp/delete_profile.html")



