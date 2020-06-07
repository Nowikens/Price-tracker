from django.shortcuts import render, redirect

from .forms import UserProfileForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register(request):
    user_form = UserCreationForm()
    profile_form = UserProfileForm()
    
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user_model = user
            profile.save()
            return redirect('index:home')
    
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'accounts/register.html', context)
    
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index:home')
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('accounts:login')
    context = {}
    return render(request, 'accounts/login.html', context)
    
    
    
def logout_user(request):
    logout(request)
    return redirect('accounts:login')
    
def change_wanted_price(request, price):
    return redirect('index:home')