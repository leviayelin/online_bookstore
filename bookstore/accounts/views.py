from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


# signup views
def signup_view(request):
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,'User signed-up successfully!')
            return redirect('store:home')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

# login views
def login_view(request):
    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'User logged-in successfully!')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('store:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# logout views
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'User logged out successfully!')
        return redirect('store:home')
